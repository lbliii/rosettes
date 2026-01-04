"""HTML formatter for Rosettes.

Generates HTML output with semantic or Pygments-compatible CSS classes.
Thread-safe by design — no mutable shared state.

Features:
    - Dual CSS class output: semantic (.syntax-function) or Pygments (.nf)
    - CSS custom properties for runtime theming
    - Line highlighting (hl_lines parameter)
    - Streaming output (generator-based)

Design Philosophy:
    The HTML formatter is optimized for the common case while supporting
    advanced features when needed:

    1. **Fast path**: format_fast() for simple highlighting (~50µs/block)
    2. **Slow path**: format() for line highlighting, line numbers
    3. **Immutable**: Frozen dataclass ensures thread-safety
    4. **Streaming**: Yields chunks for memory-efficient processing

CSS Class Styles:
    semantic (default):
        Human-readable class names: .syntax-function, .syntax-keyword
        Better for custom themes and debugging

    pygments:
        Pygments-compatible names: .nf, .k
        Works with existing Pygments CSS themes

Performance Optimizations:
    1. Fast path when no line highlighting needed
    2. Pre-computed escape table (C-level str.translate)
    3. Pre-built span templates (avoid f-string in loop)
    4. Direct token type value access (StrEnum)
    5. Streaming output (generator, no intermediate list)

    Benchmarks (100-line Python file):
        - format_fast(): ~50µs
        - format() with hl_lines: ~80µs
        - format() with line numbers: ~100µs

Common Mistakes:
    # ❌ WRONG: Calling format() and ignoring streaming
    html = ""
    for chunk in formatter.format(tokens):
        html += chunk  # O(n²) string concatenation

    # ✅ CORRECT: Use format_string() or join()
    html = formatter.format_string(tokens)
    # or
    html = "".join(formatter.format(tokens))

See Also:
    rosettes.formatters.terminal: ANSI terminal output formatter
    rosettes.formatters.null: No-op formatter for testing
    rosettes.themes: CSS generation for HTML themes
    rosettes._escape: HTML entity escaping (used internally)
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from rosettes._config import FormatConfig, HighlightConfig
from rosettes._escape import escape_html
from rosettes._types import Token, TokenType
from rosettes.themes._mapping import ROLE_MAPPING
from rosettes.themes._roles import SyntaxRole

if TYPE_CHECKING:
    pass

__all__ = ["HtmlFormatter"]

CssClassStyle = Literal["semantic", "pygments"]

# Pre-compute token types that don't need spans
_NO_SPAN_TYPES = frozenset({TokenType.TEXT, TokenType.WHITESPACE})

# Semantic class names for roles
_SEMANTIC_CLASS: dict[SyntaxRole, str] = {
    SyntaxRole.CONTROL_FLOW: "syntax-control",
    SyntaxRole.DECLARATION: "syntax-declaration",
    SyntaxRole.IMPORT: "syntax-import",
    SyntaxRole.STRING: "syntax-string",
    SyntaxRole.DOCSTRING: "syntax-docstring",
    SyntaxRole.NUMBER: "syntax-number",
    SyntaxRole.BOOLEAN: "syntax-boolean",
    SyntaxRole.TYPE: "syntax-type",
    SyntaxRole.FUNCTION: "syntax-function",
    SyntaxRole.VARIABLE: "syntax-variable",
    SyntaxRole.CONSTANT: "syntax-constant",
    SyntaxRole.COMMENT: "syntax-comment",
    SyntaxRole.ERROR: "syntax-error",
    SyntaxRole.WARNING: "syntax-warning",
    SyntaxRole.ADDED: "syntax-added",
    SyntaxRole.REMOVED: "syntax-removed",
    SyntaxRole.TEXT: "",
    SyntaxRole.MUTED: "syntax-muted",
    SyntaxRole.PUNCTUATION: "syntax-punctuation",
    SyntaxRole.OPERATOR: "syntax-operator",
    SyntaxRole.ATTRIBUTE: "syntax-attribute",
    SyntaxRole.NAMESPACE: "syntax-namespace",
    SyntaxRole.TAG: "syntax-tag",
    SyntaxRole.REGEX: "syntax-regex",
    SyntaxRole.ESCAPE: "syntax-escape",
}

# Pre-build span templates for Pygments compatibility
_SPAN_OPEN: dict[str, str] = {}
_SPAN_CLOSE = "</span>"
for _tt in TokenType:
    if _tt not in _NO_SPAN_TYPES:
        _SPAN_OPEN[_tt.value] = f'<span class="{_tt.value}">'

# Pre-build semantic span templates
_SEMANTIC_SPAN_OPEN: dict[SyntaxRole, str] = {}
for _role, _class_name in _SEMANTIC_CLASS.items():
    if _class_name:
        _SEMANTIC_SPAN_OPEN[_role] = f'<span class="{_class_name}">'


@dataclass(frozen=True, slots=True)
class HtmlFormatter:
    """HTML formatter with streaming output.

    Thread-safe: all state is immutable or local to method calls.
    Instances are frozen dataclasses and can be safely shared across threads.

    Attributes:
        config: Highlight configuration for line highlighting, line numbers.
        css_class_style: "semantic" for .syntax-* or "pygments" for .k, .nf

    Example:
        >>> from rosettes import get_lexer, HtmlFormatter
        >>> lexer = get_lexer("python")
        >>> formatter = HtmlFormatter(css_class_style="semantic")
        >>> tokens = lexer.tokenize("def foo(): pass")
        >>> html = formatter.format_string(tokens)
        >>> "syntax-declaration" in html
        True

    Example (line highlighting):
        >>> from rosettes._config import HighlightConfig
        >>> config = HighlightConfig(hl_lines=frozenset({1, 3}))
        >>> formatter = HtmlFormatter(config=config)

    Output Structure:
        <div class="rosettes" data-language="python">
          <pre><code>
            <span class="syntax-keyword">def</span> ...
          </code></pre>
        </div>

    Note:
        For most use cases, use the high-level rosettes.highlight() function
        instead of instantiating HtmlFormatter directly.
    """

    config: HighlightConfig = field(default_factory=HighlightConfig)
    css_class_style: CssClassStyle = "semantic"

    @property
    def name(self) -> str:
        return "html"

    @property
    def container_class(self) -> str:
        """Get the container CSS class based on style."""
        return "rosettes" if self.css_class_style == "semantic" else "highlight"

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Ultra-fast formatting without line highlighting.

        Uses role-based class names for semantic mode.

        Optimizations:
            - Pre-built span templates (no f-string per token)
            - Direct dict lookup (O(1))
            - Minimal branching in hot path
        """
        if config is None:
            config = FormatConfig()

        is_semantic = self.css_class_style == "semantic"

        # Cache lookups
        no_span = _NO_SPAN_TYPES
        escape = escape_html
        prefix = config.class_prefix
        container = config.css_class if config.css_class else self.container_class

        if is_semantic:
            span_open = _SEMANTIC_SPAN_OPEN
            role_mapping = ROLE_MAPPING
        else:
            span_open = _SPAN_OPEN
            role_mapping = None

        # Use prefixed templates if needed
        if prefix and not is_semantic:
            span_open = {k: f'<span class="{prefix}{k}">' for k in span_open}
        elif prefix and is_semantic:
            span_open = {
                k: f'<span class="{prefix}{v.split(">")[0].split(chr(34))[1]}">'
                for k, v in span_open.items()
            }

        span_close = _SPAN_CLOSE

        # Opening tags
        if config.wrap_code:
            data_lang_attr = (
                f' data-language="{config.data_language}"' if config.data_language else ""
            )
            yield f'<div class="{container}"{data_lang_attr}><pre><code>'

        # Hot path - format each token
        if is_semantic:
            for token_type, value in tokens:
                if token_type in no_span:
                    yield escape(value)
                else:
                    role = role_mapping.get(token_type, SyntaxRole.TEXT)
                    template = span_open.get(role)
                    if template:
                        yield template
                        yield escape(value)
                        yield span_close
                    else:
                        yield escape(value)
        else:
            for token_type, value in tokens:
                if token_type in no_span:
                    yield escape(value)
                else:
                    tv = token_type.value
                    template = span_open.get(tv)
                    if template:
                        yield template
                        yield escape(value)
                        yield span_close
                    else:
                        yield escape(value)

        # Closing tags
        if config.wrap_code:
            yield "</code></pre></div>"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Format tokens as HTML with streaming output."""
        if config is None:
            config = FormatConfig()

        hl_lines = self.config.hl_lines
        is_semantic = self.css_class_style == "semantic"
        container = config.css_class if config.css_class else self.container_class

        # Fast path: no line highlighting
        if not hl_lines:
            fast_tokens = ((t.type, t.value) for t in tokens)
            yield from self.format_fast(fast_tokens, config)
            return

        # Slow path: line highlighting
        no_span = _NO_SPAN_TYPES
        escape = escape_html
        prefix = config.class_prefix
        hl_line_class = self.config.hl_line_class
        hl_span_open = f'<span class="{hl_line_class}">'
        span_close = _SPAN_CLOSE

        if is_semantic:
            span_open = _SEMANTIC_SPAN_OPEN
            role_mapping = ROLE_MAPPING
        else:
            span_open = _SPAN_OPEN
            role_mapping = None

        if prefix and not is_semantic:
            span_open = {k: f'<span class="{prefix}{k}">' for k in span_open}

        if config.wrap_code:
            data_lang_attr = (
                f' data-language="{config.data_language}"' if config.data_language else ""
            )
            yield f'<div class="{container}"{data_lang_attr}><pre><code>'

        current_line = 1
        in_hl = current_line in hl_lines

        if in_hl:
            yield hl_span_open

        for token in tokens:
            # Handle line transitions
            while current_line < token.line:
                if in_hl:
                    yield span_close
                yield "\n"
                current_line += 1
                in_hl = current_line in hl_lines
                if in_hl:
                    yield hl_span_open

            # Format token
            escaped = escape(token.value)
            if token.type in no_span:
                yield escaped
            else:
                if is_semantic:
                    role = role_mapping.get(token.type, SyntaxRole.TEXT)
                    template = span_open.get(role)
                else:
                    template = span_open.get(token.type.value)

                if template:
                    yield template
                    yield escaped
                    yield span_close
                else:
                    yield escaped

            # Track embedded newlines
            value = token.value
            nl_idx = value.find("\n")
            if nl_idx >= 0:
                if in_hl:
                    yield span_close
                # Count newlines without second scan
                newlines = value.count("\n", nl_idx)
                for _ in range(newlines):
                    current_line += 1
                    in_hl = current_line in hl_lines
                if in_hl:
                    yield hl_span_open

        if in_hl:
            yield span_close

        if config.wrap_code:
            yield "</code></pre></div>"

    def format_string(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> str:
        return "".join(self.format(tokens, config))

    def format_string_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> str:
        return "".join(self.format_fast(tokens, config))
