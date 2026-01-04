"""Lazy formatter registry for Rosettes.

Formatters are loaded on-demand using functools.cache for thread-safe memoization.

Design Philosophy:
    Mirrors the lexer registry pattern (see rosettes._registry) for consistency:

    1. **Lazy loading**: Formatter modules imported only on first use
    2. **Cached instances**: functools.cache ensures one instance per formatter
    3. **Alias support**: Multiple names resolve to the same formatter
    4. **Thread-safe**: cache is thread-safe; formatters are immutable

Architecture:
    _FORMATTER_SPECS: Static mapping of names to (module, class) specs
    _ALIAS_TO_NAME: Case-insensitive alias lookup
    _get_formatter_by_canonical: Cached formatter instantiation

Available Formatters:
    html: HTML output with semantic or Pygments CSS classes
    terminal: ANSI escape codes for terminal output
    null: No-op formatter for benchmarking/testing

Performance:
    - First call: ~0.5ms (module import + instantiation)
    - Subsequent calls: ~100ns (dict lookup + cache hit)

Common Mistakes:
    # ❌ WRONG: Caching formatter instances
    formatters = {"html": get_formatter("html")}

    # ✅ CORRECT: Just call get_formatter() — already cached
    formatter = get_formatter("html")

See Also:
    rosettes._registry: Lexer registry (same pattern)
    rosettes._protocol.Formatter: Protocol that formatters implement
    rosettes.formatters: Formatter implementations
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._protocol import Formatter

__all__ = ["get_formatter", "list_formatters", "supports_formatter"]


@dataclass(frozen=True, slots=True)
class FormatterSpec:
    """Specification for lazy-loading a formatter.

    Attributes:
        module: Full module path (e.g., 'rosettes.formatters.html').
        class_name: Name of the formatter class in the module.
        aliases: Alternative names for lookup.
    """

    module: str
    class_name: str
    aliases: tuple[str, ...] = ()


# Static registry of formatters
_FORMATTER_SPECS: dict[str, FormatterSpec] = {
    "html": FormatterSpec(
        "rosettes.formatters.html",
        "HtmlFormatter",
        aliases=("htm",),
    ),
    "terminal": FormatterSpec(
        "rosettes.formatters.terminal",
        "TerminalFormatter",
        aliases=("ansi", "console"),
    ),
    "null": FormatterSpec(
        "rosettes.formatters.null",
        "NullFormatter",
        aliases=("none",),
    ),
}

# Build alias lookup table
_ALIAS_TO_NAME: dict[str, str] = {}
for _name, _spec in _FORMATTER_SPECS.items():
    _ALIAS_TO_NAME[_name] = _name
    for _alias in _spec.aliases:
        _ALIAS_TO_NAME[_alias] = _name

# Pre-compute sorted list
_SORTED_FORMATTERS: list[str] = sorted(_FORMATTER_SPECS.keys())


def get_formatter(name: str) -> Formatter:
    """Get a formatter instance by name or alias.

    Args:
        name: Formatter name or alias (e.g., 'html', 'terminal').

    Returns:
        Formatter instance.

    Raises:
        LookupError: If the formatter is not supported.
    """
    lower = name.lower()
    if lower not in _ALIAS_TO_NAME:
        raise LookupError(f"Unknown formatter: {name!r}. Supported: {_SORTED_FORMATTERS}")

    canonical = _ALIAS_TO_NAME[lower]
    return _get_formatter_by_canonical(canonical)


@cache
def _get_formatter_by_canonical(canonical: str) -> Formatter:
    """Internal cached loader."""
    spec = _FORMATTER_SPECS[canonical]
    module = import_module(spec.module)
    formatter_class = getattr(module, spec.class_name)
    return formatter_class()


def list_formatters() -> list[str]:
    """List all supported formatter names."""
    return _SORTED_FORMATTERS.copy()


def supports_formatter(name: str) -> bool:
    """Check if a formatter is supported."""
    return name.lower() in _ALIAS_TO_NAME
