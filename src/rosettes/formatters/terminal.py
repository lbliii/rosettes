"""Terminal formatter for Rosettes.

Generates ANSI-colored output for terminal consoles.
Thread-safe and optimized for streaming.

Design Philosophy:
    The terminal formatter maps semantic syntax roles to ANSI color codes.
    It uses the same role-based system as the HTML formatter, ensuring
    visual consistency between terminal and web output.

ANSI Color Mapping:
    Control/Declaration: Magenta/Cyan (stand out for structure)
    Strings: Green (universally recognized)
    Numbers: Yellow (distinct from strings)
    Functions: Blue (clear identifier category)
    Comments: Gray (de-emphasized)
    Errors: Red (universal error color)

Performance:
    - Pre-computed token-to-ANSI mapping (~100 entries)
    - O(1) color lookup per token
    - Streaming output (yields chunks, no intermediate list)

    Benchmarks:
        ~30µs per 100-line file (vs ~50µs for HTML)

Terminal Compatibility:
    Uses standard ANSI SGR (Select Graphic Rendition) codes:
    - \\033[XXm for color (30-37 normal, 90-97 bright)
    - \\033[0m for reset

    Compatible with:
    - Modern terminals (iTerm2, Windows Terminal, GNOME Terminal)
    - VS Code integrated terminal
    - Most CI/CD log viewers

Thread-Safety:
    The formatter is a frozen dataclass with no mutable state.
    Color mappings are module-level constants (immutable dicts).

See Also:
    rosettes.formatters.html: HTML output (same role system)
    rosettes.themes._roles: Semantic role definitions
    rosettes.themes._mapping: TokenType → SyntaxRole mapping
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

from rosettes._types import Token, TokenType
from rosettes.themes._mapping import ROLE_MAPPING
from rosettes.themes._roles import SyntaxRole

if TYPE_CHECKING:
    from rosettes._config import FormatConfig

__all__ = ["TerminalFormatter"]

# ANSI Color Codes
_RESET = "\033[0m"
_BOLD = "\033[1m"

_ANSI_COLORS: dict[SyntaxRole, str] = {
    SyntaxRole.CONTROL_FLOW: "\033[35m",  # Magenta
    SyntaxRole.DECLARATION: "\033[36m",  # Cyan
    SyntaxRole.IMPORT: "\033[35m",  # Magenta
    SyntaxRole.STRING: "\033[32m",  # Green
    SyntaxRole.DOCSTRING: "\033[90m",  # Gray
    SyntaxRole.NUMBER: "\033[33m",  # Yellow
    SyntaxRole.BOOLEAN: "\033[33m",  # Yellow
    SyntaxRole.TYPE: "\033[36m",  # Cyan
    SyntaxRole.FUNCTION: "\033[34m",  # Blue
    SyntaxRole.VARIABLE: "\033[37m",  # White
    SyntaxRole.CONSTANT: "\033[33m",  # Yellow
    SyntaxRole.COMMENT: "\033[90m",  # Gray
    SyntaxRole.ERROR: "\033[31m",  # Red
    SyntaxRole.WARNING: "\033[33m",  # Yellow
    SyntaxRole.ADDED: "\033[32m",  # Green
    SyntaxRole.REMOVED: "\033[31m",  # Red
    SyntaxRole.MUTED: "\033[90m",  # Gray
    SyntaxRole.PUNCTUATION: "\033[37m",  # White
    SyntaxRole.OPERATOR: "\033[37m",  # White
    SyntaxRole.ATTRIBUTE: "\033[36m",  # Cyan
    SyntaxRole.NAMESPACE: "\033[35m",  # Magenta
    SyntaxRole.TAG: "\033[34m",  # Blue
    SyntaxRole.REGEX: "\033[32m",  # Green
    SyntaxRole.ESCAPE: "\033[33m",  # Yellow
}

# Pre-compute token-to-ANSI mapping for maximum performance in hot path
_TOKEN_ANSI_START: dict[TokenType, str] = {}
for _tt in TokenType:
    _role = ROLE_MAPPING.get(_tt, SyntaxRole.TEXT)
    _color = _ANSI_COLORS.get(_role)
    if _color:
        _TOKEN_ANSI_START[_tt] = _color

_NO_COLOR_TYPES = {TokenType.TEXT, TokenType.WHITESPACE}


@dataclass(frozen=True, slots=True)
class TerminalFormatter:
    """ANSI color formatter for terminals.

    Thread-safe: frozen dataclass with no mutable state.
    Uses pre-computed color mappings for O(1) lookup per token.

    Example:
        >>> from rosettes import highlight
        >>> ansi = highlight("def foo(): pass", "python", formatter="terminal")
        >>> print(ansi)  # Colored output in terminal

    Example (direct usage):
        >>> from rosettes import get_lexer
        >>> from rosettes.formatters import TerminalFormatter
        >>> lexer = get_lexer("python")
        >>> formatter = TerminalFormatter()
        >>> output = formatter.format_string(lexer.tokenize("x = 1"))

    Note:
        For most use cases, use rosettes.highlight() with formatter="terminal"
        instead of instantiating TerminalFormatter directly.
    """

    @property
    def name(self) -> str:
        return "terminal"

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Fast ANSI formatting using pre-computed color maps."""
        ansi_start = _TOKEN_ANSI_START
        no_color = _NO_COLOR_TYPES
        reset = _RESET

        for tt, value in tokens:
            if tt in no_color:
                yield value
            else:
                color = ansi_start.get(tt)
                if color:
                    yield color
                    yield value
                    yield reset
                else:
                    yield value

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Format tokens as ANSI-colored strings."""
        ansi_start = _TOKEN_ANSI_START
        no_color = _NO_COLOR_TYPES
        reset = _RESET

        for token in tokens:
            tt = token.type
            if tt in no_color:
                yield token.value
            else:
                color = ansi_start.get(tt)
                if color:
                    yield color
                    yield token.value
                    yield reset
                else:
                    yield token.value

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
