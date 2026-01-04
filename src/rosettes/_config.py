"""Frozen configuration dataclasses for Rosettes.

All configuration objects are immutable (frozen) for thread-safety.

Design Philosophy:
    Configuration in Rosettes uses frozen dataclasses to ensure:

    1. **Thread-Safety**: Immutable state can be safely shared across threads
    2. **Predictability**: Config cannot change after creation
    3. **Performance**: slots=True reduces memory overhead

Configuration Types:
    LexerConfig: Controls lexer behavior (whitespace handling, tab size)
    FormatConfig: Controls formatter output (CSS class, wrapping)
    HighlightConfig: Controls highlighting (line numbers, hl_lines)

Usage:
    Most users don't need to create config objects directly — the high-level
    highlight() function accepts keyword arguments that create configs internally.

    Direct config usage is for:
        - Custom formatters needing specific settings
        - Reusing config across multiple highlight calls
        - Unit testing with controlled configuration

See Also:
    rosettes.highlight: High-level API that accepts config via kwargs
    rosettes.formatters.html.HtmlFormatter: Uses HighlightConfig
"""

from dataclasses import dataclass

__all__ = ["LexerConfig", "FormatConfig", "HighlightConfig"]


@dataclass(frozen=True, slots=True)
class LexerConfig:
    """Configuration for lexer behavior.

    Attributes:
        strip_whitespace: If True, strip trailing whitespace from lines.
        tab_size: Number of spaces per tab for column calculation.
    """

    strip_whitespace: bool = False
    tab_size: int = 4


@dataclass(frozen=True, slots=True)
class FormatConfig:
    """Configuration for output formatting.

    Attributes:
        css_class: Base CSS class for the code container.
        wrap_code: If True, wrap output in <pre><code> tags.
        class_prefix: Prefix for token CSS classes.
        data_language: Language name for data-language attribute (e.g., 'python').
    """

    css_class: str = "highlight"
    wrap_code: bool = True
    class_prefix: str = ""
    data_language: str | None = None


@dataclass(frozen=True, slots=True)
class HighlightConfig:
    """Combined configuration for syntax highlighting.

    Attributes:
        hl_lines: Set of 1-based line numbers to highlight.
        show_linenos: If True, include line numbers in output.
        css_class: Base CSS class for the code container.
        lineno_class: CSS class for line number elements.
        hl_line_class: CSS class for highlighted lines.
    """

    hl_lines: frozenset[int] = frozenset()
    show_linenos: bool = False
    css_class: str = "highlight"
    lineno_class: str = "lineno"
    hl_line_class: str = "hll"
