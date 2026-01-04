"""Base class for hand-written state machine lexers.

Thread-safe, O(n) guaranteed, zero regex.

Design Philosophy:
    Rosettes lexers are hand-written state machines rather than regex-based.
    This design provides:

    1. **Security**: No ReDoS vulnerability. Crafted input cannot cause
       exponential backtracking because there IS no backtracking.

    2. **Performance**: O(n) guaranteed. Single pass, character by character.
       Predictable performance regardless of input.

    3. **Thread-Safety**: Each tokenize() call uses only local variables.
       No shared mutable state means true parallelism on Python 3.14t.

    4. **Debuggability**: Explicit state transitions are easier to trace
       than regex match failures.

Architecture:
    StateMachineLexer provides:
        - Base class with shared character sets (DIGITS, IDENT_START, etc.)
        - Default tokenize_fast() implementation
        - Protocol-compatible interface

    Helper functions provide common patterns:
        - scan_while(): Advance while chars match set
        - scan_until(): Advance until char in set
        - scan_string(): Handle quoted strings with escapes
        - scan_triple_string(): Handle triple-quoted strings
        - scan_line_comment(): Scan to end of line
        - scan_block_comment(): Scan to end marker

Adding New Languages:
    To add a new language lexer:

    1. Create rosettes/lexers/{language}_sm.py
    2. Subclass StateMachineLexer
    3. Set name, aliases, filenames, mimetypes class attributes
    4. Implement tokenize() method with character-by-character logic
    5. Add entry to _LEXER_SPECS in rosettes/_registry.py
    6. Add tests in tests/lexers/test_{language}_sm.py

    Example skeleton:
        class MyLangStateMachineLexer(StateMachineLexer):
            name = "mylang"
            aliases = ("ml",)
            filenames = ("*.ml",)
            mimetypes = ("text/x-mylang",)

            # Language-specific character sets
            KEYWORDS = frozenset({"if", "else", "while"})

            def tokenize(self, code, config=None, start=0, end=None):
                # Your tokenization logic here
                ...

    Key rules:
        - Use only local variables (no self.state mutations)
        - Yield tokens as you find them (streaming)
        - Handle all characters (emit TEXT for unknown)
        - Use helper functions for common patterns

Performance Tips:
    - Use frozenset for keyword/operator lookups (O(1))
    - Use scan_while/scan_until helpers for common patterns
    - Avoid string slicing in hot loops (use start/end indices)
    - Pre-compute character sets as class attributes

See Also:
    rosettes/_protocol.Lexer: Protocol that all lexers must satisfy
    rosettes/_registry: How lexers are registered and looked up
    rosettes/lexers/python_sm.py: Reference implementation
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType

if TYPE_CHECKING:
    pass

__all__ = [
    "StateMachineLexer",
    "scan_while",
    "scan_until",
    "scan_string",
    "scan_triple_string",
]


class StateMachineLexer:
    """Base class for hand-written state machine lexers.

    Thread-safe: tokenize() uses only local variables.
    O(n) guaranteed: single pass, no backtracking.

    Subclasses implement language-specific tokenization by overriding
    the tokenize() method with character-by-character logic.

    Design Principles:
        1. No regex — character matching only
        2. Explicit state — no hidden backtracking
        3. Local variables only — thread-safe by design
        4. Single pass — O(n) guaranteed

    Class Attributes:
        name: Canonical language name (e.g., 'python')
        aliases: Alternative names for registry lookup (e.g., ('py', 'python3'))
        filenames: Glob patterns for file detection (e.g., ('*.py',))
        mimetypes: MIME types for content detection

    Shared Character Sets:
        DIGITS: '0'-'9'
        HEX_DIGITS: '0'-'9', 'a'-'f', 'A'-'F'
        LETTERS: 'a'-'z', 'A'-'Z'
        IDENT_START: Letters + '_'
        IDENT_CONT: IDENT_START + digits
        WHITESPACE: Space, tab, newline, etc.

    Example Implementation:
        class MyLangLexer(StateMachineLexer):
            name = "mylang"
            aliases = ("ml",)
            KEYWORDS = frozenset({"if", "else"})

            def tokenize(self, code, config=None, start=0, end=None):
                pos = start
                end = end or len(code)
                line, col = 1, 1

                while pos < end:
                    char = code[pos]
                    # ... tokenization logic ...
                    yield Token(TokenType.TEXT, char, line, col)
                    pos += 1
                    col += 1

    Common Mistakes:
        # ❌ WRONG: Storing state in instance variables
        self.current_line = 1  # NOT thread-safe!

        # ✅ CORRECT: Use local variables
        line = 1

        # ❌ WRONG: Using regex for matching
        match = re.match(r'\\d+', code[pos:])  # ReDoS vulnerable!

        # ✅ CORRECT: Use scan_while helper
        end_pos = scan_while(code, pos, self.DIGITS)
    """

    name: str = "base"
    aliases: tuple[str, ...] = ()
    filenames: tuple[str, ...] = ()
    mimetypes: tuple[str, ...] = ()

    # Shared character class sets (frozen for thread safety)
    DIGITS: frozenset[str] = frozenset("0123456789")
    HEX_DIGITS: frozenset[str] = frozenset("0123456789abcdefABCDEF")
    OCTAL_DIGITS: frozenset[str] = frozenset("01234567")
    BINARY_DIGITS: frozenset[str] = frozenset("01")
    LETTERS: frozenset[str] = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    IDENT_START: frozenset[str] = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")
    IDENT_CONT: frozenset[str] = frozenset(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"
    )
    WHITESPACE: frozenset[str] = frozenset(" \t\n\r\f\v")

    def tokenize(
        self,
        code: str,
        config: LexerConfig | None = None,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]:
        """Tokenize source code.

        Subclasses override this with language-specific logic.

        Args:
            code: The source code to tokenize.
            config: Optional lexer configuration.
            start: Starting index in the source string.
            end: Optional ending index in the source string.

        Yields:
            Token objects in order of appearance.
        """
        raise NotImplementedError("Subclasses must implement tokenize()")

    def tokenize_fast(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[tuple[TokenType, str]]:
        """Fast tokenization without position tracking.

        Default implementation strips position info from tokenize().
        Subclasses may override for further optimization.

        Args:
            code: The source code to tokenize.
            start: Starting index in the source string.
            end: Optional ending index in the source string.

        Yields:
            (TokenType, value) tuples.
        """
        for token in self.tokenize(code, start=start, end=end):
            yield (token.type, token.value)


# =============================================================================
# Helper functions for common scanning patterns
# =============================================================================


def scan_while(code: str, pos: int, char_set: frozenset[str]) -> int:
    """Advance position while characters are in char_set.

    Args:
        code: Source code string.
        pos: Starting position.
        char_set: Set of characters to match.

    Returns:
        The new position (may be unchanged if no match).
    """
    length = len(code)
    while pos < length and code[pos] in char_set:
        pos += 1
    return pos


def scan_until(code: str, pos: int, char_set: frozenset[str]) -> int:
    """Advance position until a character in char_set is found.

    Args:
        code: Source code string.
        pos: Starting position.
        char_set: Set of characters to stop at.

    Returns:
        The new position (may be end of string).
    """
    length = len(code)
    while pos < length and code[pos] not in char_set:
        pos += 1
    return pos


def scan_string(
    code: str,
    pos: int,
    quote: str,
    *,
    allow_escape: bool = True,
    allow_multiline: bool = False,
) -> int:
    """Scan a string literal, handling escapes.

    Args:
        code: Source code.
        pos: Position after opening quote.
        quote: The quote character (' or ").
        allow_escape: Whether backslash escapes are allowed.
        allow_multiline: Whether newlines are allowed.

    Returns:
        Position after closing quote (or end of string/line if unterminated).
    """
    length = len(code)

    while pos < length:
        char = code[pos]

        if char == quote:
            return pos + 1  # Include closing quote

        if char == "\\" and allow_escape and pos + 1 < length:
            pos += 2  # Skip escape sequence
            continue

        if char == "\n" and not allow_multiline:
            return pos  # Unterminated string

        pos += 1

    return pos  # End of input (unterminated)


def scan_triple_string(code: str, pos: int, quote: str) -> int:
    """Scan a triple-quoted string.

    Args:
        code: Source code.
        pos: Position after opening triple quote.
        quote: The quote character (' or ").

    Returns:
        Position after closing triple quote (or end of input).
    """
    length = len(code)
    triple = quote * 3

    while pos < length:
        if code[pos : pos + 3] == triple:
            return pos + 3

        if code[pos] == "\\" and pos + 1 < length:
            pos += 2  # Skip escape
            continue

        pos += 1

    return pos  # End of input (unterminated)


def scan_line_comment(code: str, pos: int) -> int:
    """Scan to end of line (for line comments).

    Args:
        code: Source code.
        pos: Starting position (after comment marker).

    Returns:
        Position at end of line (before newline) or end of input.
    """
    length = len(code)
    while pos < length and code[pos] != "\n":
        pos += 1
    return pos


def scan_block_comment(code: str, pos: int, end_marker: str) -> int:
    """Scan a block comment until end marker.

    Args:
        code: Source code.
        pos: Position after opening marker.
        end_marker: The closing marker (e.g., "*/" or "-->").

    Returns:
        Position after closing marker (or end of input).
    """
    length = len(code)
    marker_len = len(end_marker)

    while pos < length:
        if code[pos : pos + marker_len] == end_marker:
            return pos + marker_len
        pos += 1

    return pos  # End of input (unterminated)
