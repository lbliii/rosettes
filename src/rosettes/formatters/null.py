"""Null formatter for Rosettes.

Does nothing but return the raw text. Useful for timing or as a fallback.
Thread-safe and optimized for streaming.

Design Philosophy:
    The null formatter exists for specific use cases where you need
    the formatter interface but don't want any transformation:

Use Cases:
    1. **Benchmarking**: Measure lexer performance without formatter overhead
    2. **Testing**: Verify tokenization without HTML/ANSI complexity
    3. **Fallback**: Handle unsupported output formats gracefully
    4. **Pipeline Integration**: When downstream expects raw text

Performance:
    The absolute minimum overhead possible:
    - format(): yield token.value (one attribute access per token)
    - format_fast(): yield value (already unpacked)

    ~5µs per 100-line file (vs ~50µs for HTML)

Example:
    >>> from rosettes import highlight
    >>> raw = highlight("def foo(): pass", "python", formatter="null")
    >>> raw
    'def foo(): pass'

See Also:
    rosettes.formatters.html: HTML output with CSS classes
    rosettes.formatters.terminal: ANSI terminal output
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rosettes._config import FormatConfig
    from rosettes._types import Token, TokenType


@dataclass(frozen=True, slots=True)
class NullFormatter:
    """Formatter that yields raw token values without any styling.

    Thread-safe: immutable dataclass with no shared state.

    This is the simplest possible formatter — it just concatenates
    token values without any transformation.

    Example:
        >>> from rosettes import get_lexer
        >>> from rosettes.formatters import NullFormatter
        >>> lexer = get_lexer("python")
        >>> formatter = NullFormatter()
        >>> output = formatter.format_string(lexer.tokenize("x = 1"))
        >>> output
        'x = 1'

    Use Cases:
        - Benchmarking lexer performance
        - Testing tokenization correctness
        - Fallback when output format is unsupported
    """

    @property
    def name(self) -> str:
        return "null"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Format tokens by yielding their raw values."""
        for token in tokens:
            yield token.value

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Fast formatting — just yield raw values."""
        for _, value in tokens:
            yield value

    def format_string(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> str:
        """Format tokens and return as a single string."""
        return "".join(self.format(tokens, config))

    def format_string_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> str:
        """Fast format and return as a single string."""
        return "".join(self.format_fast(tokens, config))
