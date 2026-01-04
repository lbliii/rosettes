"""Core types for Rosettes syntax highlighting.

Thread-safe, immutable types for tokenization.

Design Philosophy:
    Types in this module are designed for maximum performance and safety:

    1. **Immutable**: Token is a NamedTuple, TokenType is a StrEnum
    2. **Minimal memory**: Token is ~64 bytes (vs ~200 for a regular object)
    3. **Hashable**: Tokens can be used in sets/dicts for deduplication
    4. **Thread-safe**: Immutability means no synchronization needed

What Goes in TokenType:
    ✅ DO include:
        - Language keywords (KEYWORD, KEYWORD_DECLARATION, etc.)
        - Operators and punctuation (OPERATOR, PUNCTUATION)
        - Literals (STRING, NUMBER, etc.)
        - Comments (COMMENT, COMMENT_MULTILINE, etc.)
        - Names (NAME, NAME_FUNCTION, NAME_CLASS, etc.)

    ❌ DON'T include:
        - Formatting hints (indentation level, line breaks)
        - Editor-specific tokens (folding markers, etc.)
        - Language-specific tokens (use generic categories)

Pygments Compatibility:
    TokenType values are the CSS class suffixes used by Pygments themes.
    This means existing Pygments stylesheets work with Rosettes output:

    - TokenType.KEYWORD = "k" → <span class="k">def</span>
    - TokenType.NAME_FUNCTION = "nf" → <span class="nf">my_func</span>

    Use css_class_style="pygments" in highlight() for this compatibility.
    Use css_class_style="semantic" for readable classes like .syntax-function.

See Also:
    rosettes.themes._roles: Higher-level semantic roles for theming
    rosettes.themes._mapping: TokenType → SyntaxRole mapping
    rosettes.formatters.html: How TokenTypes become CSS classes
"""

from enum import StrEnum
from typing import NamedTuple

__all__ = ["TokenType", "Token"]


class TokenType(StrEnum):
    """Semantic token types with Pygments-compatible CSS class names.

    Each value is the CSS class suffix used by Pygments themes.
    This ensures drop-in compatibility with existing Pygments stylesheets.

    Categories:
        Keywords: KEYWORD, KEYWORD_CONSTANT, KEYWORD_DECLARATION, etc.
        Names: NAME, NAME_FUNCTION, NAME_CLASS, NAME_BUILTIN, etc.
        Literals: STRING, NUMBER, NUMBER_FLOAT, etc.
        Operators: OPERATOR, OPERATOR_WORD
        Punctuation: PUNCTUATION, PUNCTUATION_MARKER
        Comments: COMMENT, COMMENT_SINGLE, COMMENT_MULTILINE, etc.
        Generic: TEXT, WHITESPACE, ERROR (for diffs, errors, etc.)

    Usage:
        >>> from rosettes import TokenType
        >>> TokenType.KEYWORD
        <TokenType.KEYWORD: 'k'>
        >>> TokenType.KEYWORD.value  # CSS class suffix
        'k'
    """

    # Keywords
    KEYWORD = "k"
    KEYWORD_CONSTANT = "kc"
    KEYWORD_DECLARATION = "kd"
    KEYWORD_NAMESPACE = "kn"
    KEYWORD_PSEUDO = "kp"
    KEYWORD_RESERVED = "kr"
    KEYWORD_TYPE = "kt"

    # Names
    NAME = "n"
    NAME_ATTRIBUTE = "na"
    NAME_BUILTIN = "nb"
    NAME_BUILTIN_PSEUDO = "bp"
    NAME_CLASS = "nc"
    NAME_CONSTANT = "no"
    NAME_DECORATOR = "nd"
    NAME_ENTITY = "ni"
    NAME_EXCEPTION = "ne"
    NAME_FUNCTION = "nf"
    NAME_FUNCTION_MAGIC = "fm"
    NAME_LABEL = "nl"
    NAME_NAMESPACE = "nn"
    NAME_OTHER = "nx"
    NAME_PROPERTY = "py"
    NAME_TAG = "nt"
    NAME_VARIABLE = "nv"
    NAME_VARIABLE_CLASS = "vc"
    NAME_VARIABLE_GLOBAL = "vg"
    NAME_VARIABLE_INSTANCE = "vi"
    NAME_VARIABLE_MAGIC = "vm"

    # Literals
    LITERAL = "l"
    LITERAL_DATE = "ld"
    STRING = "s"
    STRING_AFFIX = "sa"
    STRING_BACKTICK = "sb"
    STRING_CHAR = "sc"
    STRING_DELIMITER = "dl"
    STRING_DOC = "sd"
    STRING_DOUBLE = "s2"
    STRING_ESCAPE = "se"
    STRING_HEREDOC = "sh"
    STRING_INTERPOL = "si"
    STRING_OTHER = "sx"
    STRING_REGEX = "sr"
    STRING_SINGLE = "s1"
    STRING_SYMBOL = "ss"
    NUMBER = "m"
    NUMBER_BIN = "mb"
    NUMBER_FLOAT = "mf"
    NUMBER_HEX = "mh"
    NUMBER_INTEGER = "mi"
    NUMBER_INTEGER_LONG = "il"
    NUMBER_OCT = "mo"

    # Operators
    OPERATOR = "o"
    OPERATOR_WORD = "ow"

    # Punctuation
    PUNCTUATION = "p"
    PUNCTUATION_MARKER = "pm"

    # Comments
    COMMENT = "c"
    COMMENT_HASHBANG = "ch"
    COMMENT_MULTILINE = "cm"
    COMMENT_PREPROC = "cp"
    COMMENT_PREPROCFILE = "cpf"
    COMMENT_SINGLE = "c1"
    COMMENT_SPECIAL = "cs"

    # Generic (for diffs, etc.)
    GENERIC = "g"
    GENERIC_DELETED = "gd"
    GENERIC_EMPH = "ge"
    GENERIC_ERROR = "gr"
    GENERIC_HEADING = "gh"
    GENERIC_INSERTED = "gi"
    GENERIC_OUTPUT = "go"
    GENERIC_PROMPT = "gp"
    GENERIC_STRONG = "gs"
    GENERIC_SUBHEADING = "gu"
    GENERIC_TRACEBACK = "gt"

    # Special
    TEXT = ""
    WHITESPACE = "w"
    ERROR = "err"
    OTHER = "x"


class Token(NamedTuple):
    """Immutable token — thread-safe, minimal memory.

    A Token represents a single lexical unit from source code. Tokens are
    immutable NamedTuples for thread-safety and memory efficiency.

    Attributes:
        type: The semantic type of the token (e.g., TokenType.KEYWORD).
        value: The actual text content of the token (e.g., "def").
        line: 1-based line number where token starts.
        column: 1-based column number where token starts.

    Memory:
        Each Token uses ~64 bytes (NamedTuple overhead + references).
        A typical 100-line Python file produces ~500 tokens (~32KB).

    Thread-Safety:
        Tokens are immutable and can be safely shared across threads.
        No defensive copying needed when passing tokens between workers.

    Example:
        >>> from rosettes import tokenize
        >>> tokens = tokenize("def foo(): pass", "python")
        >>> tokens[0]
        Token(type=<TokenType.KEYWORD: 'k'>, value='def', line=1, column=1)
        >>> tokens[0].type
        <TokenType.KEYWORD: 'k'>
        >>> tokens[0].value
        'def'

    Fast Path:
        When position info is not needed, use tokenize_fast() which yields
        (TokenType, str) tuples instead of Token objects for ~20% speedup.
    """

    type: TokenType
    value: str
    line: int = 1
    column: int = 1
