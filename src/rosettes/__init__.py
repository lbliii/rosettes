"""Rosettes — Modern syntax highlighting for Python 3.14t.

A pure-Python syntax highlighter designed for free-threaded Python.
All lexers are hand-written state machines with O(n) guaranteed performance
and zero ReDoS vulnerability.

Example:
    >>> from rosettes import highlight
    >>> html = highlight("def foo(): pass", "python")
    >>> print(html)
    <div class="highlight">...</div>

Thread-Safety:
    All public APIs are thread-safe by design:
    - Lexers use only local variables during tokenization
    - Formatter state is immutable
    - Registry uses functools.cache for thread-safe memoization

Parallel Processing (3.14t):
    Rosettes supports parallel tokenization for maximum performance on
    free-threaded Python. Use highlight_many() for multiple code blocks
    or tokenize_parallel() for large single files.

Free-Threading Declaration:
    This module declares itself safe for free-threaded Python via
    the _Py_mod_gil attribute (PEP 703).
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from rosettes._config import FormatConfig, HighlightConfig, LexerConfig
from rosettes._formatter_registry import get_formatter, list_formatters, supports_formatter
from rosettes._protocol import Formatter, Lexer
from rosettes._registry import (
    get_lexer,
    list_languages,
    supports_language,
)
from rosettes._types import Token, TokenType
from rosettes.formatters import HtmlFormatter

if TYPE_CHECKING:
    from collections.abc import Iterable

__version__ = "0.1.0"

__all__ = [
    # Version
    "__version__",
    # Types
    "Token",
    "TokenType",
    # Protocols
    "Lexer",
    "Formatter",
    # Configuration
    "LexerConfig",
    "FormatConfig",
    "HighlightConfig",
    # Registry
    "get_lexer",
    "list_languages",
    "supports_language",
    "get_formatter",
    "list_formatters",
    "supports_formatter",
    # Formatters
    "HtmlFormatter",
    # High-level API
    "highlight",
    "tokenize",
    # Parallel API (3.14t optimized)
    "highlight_many",
    "tokenize_many",
]


def highlight(
    code: str,
    language: str,
    formatter: str | Formatter = "html",
    *,
    hl_lines: set[int] | frozenset[int] | None = None,
    show_linenos: bool = False,
    css_class: str | None = None,
    css_class_style: str = "semantic",
    start: int = 0,
    end: int | None = None,
) -> str:
    """Highlight source code and return formatted output.

    This is the primary high-level API for syntax highlighting.
    Thread-safe and suitable for concurrent use.

    All lexers are hand-written state machines with O(n) guaranteed
    performance and zero ReDoS vulnerability.

    Args:
        code: The source code to highlight.
        language: Language name or alias (e.g., 'python', 'py', 'js').
        formatter: Formatter name ('html', 'terminal', 'null') or instance.
        hl_lines: Optional set of 1-based line numbers to highlight.
        show_linenos: If True, include line numbers in output.
        css_class: Base CSS class for the code container (HTML only).
            Defaults to "rosettes" for semantic style, "highlight" for pygments.
        css_class_style: Class naming style (HTML only):
            - "semantic" (default): Uses readable classes like .syntax-function
            - "pygments": Uses Pygments-compatible classes like .nf
        start: Starting index in the source string.
        end: Optional ending index in the source string.

    Returns:
        Formatted string with syntax-highlighted code.

    Raises:
        LookupError: If the language or formatter is not supported.

    Example:
        >>> html = highlight("print('hello')", "python")
        >>> "rosettes" in html
        True

        >>> # Use terminal output
        >>> ansi = highlight("print('hello')", "python", formatter="terminal")
        >>> "\\033[" in ansi
        True
    """
    lexer = get_lexer(language)
    canonical_language = lexer.name

    # Resolve formatter
    if isinstance(formatter, str):
        formatter_inst = get_formatter(formatter)
    else:
        formatter_inst = formatter

    # Determine container class based on style
    if css_class is None:
        css_class = "rosettes" if css_class_style == "semantic" else "highlight"

    # Fast path: all formatters implement format_string_fast via protocol
    # Requires: no line numbers, no highlighted lines
    if not hl_lines and not show_linenos:
        # Apply HTML-specific configuration if it's an HtmlFormatter
        if isinstance(formatter_inst, HtmlFormatter):
            if formatter_inst.css_class_style != css_class_style:
                formatter_inst = HtmlFormatter(css_class_style=css_class_style)

        format_config = FormatConfig(css_class=css_class, data_language=canonical_language)
        return formatter_inst.format_string_fast(
            lexer.tokenize_fast(code, start=start, end=end), format_config
        )

    # Slow path: for line highlighting, line numbers, or formatters without fast path
    format_config = FormatConfig(css_class=css_class, data_language=canonical_language)
    hl_config = HighlightConfig(
        hl_lines=frozenset(hl_lines) if hl_lines else frozenset(),
        show_linenos=show_linenos,
        css_class=css_class,
    )

    # Re-instantiate HtmlFormatter with slow-path config if needed
    if isinstance(formatter_inst, HtmlFormatter):
        if formatter_inst.config != hl_config or formatter_inst.css_class_style != css_class_style:
            formatter_inst = HtmlFormatter(config=hl_config, css_class_style=css_class_style)

    return "".join(
        formatter_inst.format(lexer.tokenize(code, start=start, end=end), config=format_config)
    )


def tokenize(
    code: str,
    language: str,
    start: int = 0,
    end: int | None = None,
) -> list[Token]:
    """Tokenize source code without formatting.

    Useful for analysis, custom formatting, or testing.
    Thread-safe.

    All lexers are hand-written state machines with O(n) guaranteed
    performance and zero ReDoS vulnerability.

    Args:
        code: The source code to tokenize.
        language: Language name or alias.
        start: Starting index in the source string.
        end: Optional ending index in the source string.

    Returns:
        List of Token objects.

    Raises:
        LookupError: If the language is not supported.

    Example:
        >>> tokens = tokenize("x = 1", "python")
        >>> tokens[0].type
        <TokenType.NAME: 'n'>
    """
    lexer = get_lexer(language)
    return list(lexer.tokenize(code, start=start, end=end))


# =============================================================================
# Parallel API (3.14t Free-Threading Optimized)
# =============================================================================


def highlight_many(
    items: Iterable[tuple[str, str]],
    *,
    formatter: str | Formatter = "html",
    max_workers: int | None = None,
    css_class_style: str = "semantic",
) -> list[str]:
    """Highlight multiple code blocks in parallel.

    This is the recommended way to highlight many code blocks concurrently.
    On Python 3.14t (free-threaded), this provides true parallelism.
    On GIL Python, it still provides benefits via I/O overlapping.

    Thread-safe by design: each lexer uses only local variables.

    Args:
        items: Iterable of (code, language) tuples.
        formatter: Formatter name or instance.
        max_workers: Maximum number of threads. Defaults to min(4, CPU count),
            which benchmarking shows to be optimal.
        css_class_style: Class naming style (HTML only).

    Returns:
        List of formatted strings in the same order as input.

    Example:
        >>> blocks = [
        ...     ("def foo(): pass", "python"),
        ...     ("const x = 1;", "javascript"),
        ... ]
        >>> results = highlight_many(blocks)
        >>> len(results)
        2
    """
    items_list = list(items)

    if not items_list:
        return []

    # For small batches, sequential is faster (thread overhead)
    if len(items_list) < 8:
        return [
            highlight(code, lang, formatter=formatter, css_class_style=css_class_style)
            for code, lang in items_list
        ]

    def _highlight_one(item: tuple[str, str]) -> str:
        code, language = item
        return highlight(code, language, formatter=formatter, css_class_style=css_class_style)

    # Optimal worker count based on benchmarking: 4 workers is sweet spot
    if max_workers is None:
        max_workers = min(4, os.cpu_count() or 4)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(_highlight_one, items_list))


def tokenize_many(
    items: Iterable[tuple[str, str]],
    *,
    max_workers: int | None = None,
) -> list[list[Token]]:
    """Tokenize multiple code blocks in parallel.

    Similar to highlight_many() but returns raw tokens instead of HTML.
    Useful for analysis, custom formatting, or when you need token data.

    Thread-safe by design: each lexer uses only local variables.

    Args:
        items: Iterable of (code, language) tuples.
        max_workers: Maximum number of threads. Defaults to min(4, CPU count).

    Returns:
        List of token lists in the same order as input.

    Example:
        >>> blocks = [
        ...     ("x = 1", "python"),
        ...     ("let y = 2;", "javascript"),
        ... ]
        >>> results = tokenize_many(blocks)
        >>> len(results)
        2
        >>> results[0][0].type
        <TokenType.NAME: 'n'>
    """
    items_list = list(items)

    if not items_list:
        return []

    # For small batches, sequential is faster
    if len(items_list) < 8:
        return [tokenize(code, lang) for code, lang in items_list]

    def _tokenize_one(item: tuple[str, str]) -> list[Token]:
        code, language = item
        return tokenize(code, language)

    # Optimal worker count based on benchmarking
    if max_workers is None:
        max_workers = min(4, os.cpu_count() or 4)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(_tokenize_one, items_list))


# Free-threading declaration (PEP 703)
def __getattr__(name: str) -> object:
    """Module-level getattr for free-threading declaration.

    This allows Python to query whether this module is safe for
    free-threaded execution without enabling the GIL.
    """
    if name == "_Py_mod_gil":
        # Signal: this module is safe for free-threading
        # 0 = Py_MOD_GIL_NOT_USED
        return 0
    raise AttributeError(f"module 'rosettes' has no attribute {name!r}")
