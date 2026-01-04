"""Semantic syntax roles for Rosettes theming.

Defines the semantic meaning of code elements, providing a layer
between token types and colors. Themes define colors for roles,
not individual tokens.

Design Philosophy:
    Why roles instead of individual token colors?

    1. **Manageability**: Themes define ~20 colors, not 100+ token colors
    2. **Consistency**: Same semantic meaning gets same color across languages
    3. **Flexibility**: Change role→color without changing token→role
    4. **Accessibility**: Easier to ensure contrast with fewer colors

Architecture:
    TokenType → SyntaxRole → Color

    Example:
        TokenType.KEYWORD_DECLARATION ("def")  →  SyntaxRole.DECLARATION  →  #61afef
        TokenType.KEYWORD_NAMESPACE ("import") →  SyntaxRole.IMPORT       →  #c678dd

Role Categories:
    Control & Structure: CONTROL_FLOW, DECLARATION, IMPORT
        For keywords that affect program flow or structure

    Data & Literals: STRING, NUMBER, BOOLEAN
        For literal values in code

    Identifiers: TYPE, FUNCTION, VARIABLE, CONSTANT
        For named code elements

    Documentation: COMMENT, DOCSTRING
        For human-readable annotations

    Feedback: ERROR, WARNING, ADDED, REMOVED
        For diagnostic or diff highlighting

Thread-Safety:
    StrEnum is immutable by design. SyntaxRole values are string constants
    that can be safely shared across threads.

See Also:
    rosettes.themes._mapping: TokenType → SyntaxRole mapping
    rosettes.themes._palette: How roles get colors
    rosettes.formatters.html: How roles become CSS classes
"""

from enum import StrEnum

__all__ = ["SyntaxRole"]


class SyntaxRole(StrEnum):
    """Semantic roles for syntax highlighting.

    Each role represents the **purpose** of a code element, not its
    syntactic category. This enables consistent theming across languages:
    a function definition in Python and JavaScript get the same color.

    The value of each role is a short CSS-friendly identifier used in
    class names like `.syntax-function` or CSS variables like `--syntax-function`.

    Categories:
        Control & Structure: Program flow and declarations
        Data & Literals: Values embedded in code
        Identifiers: Named elements (functions, variables, types)
        Documentation: Comments and docstrings
        Feedback: Errors, warnings, diff markers

    Example:
        >>> SyntaxRole.FUNCTION
        <SyntaxRole.FUNCTION: 'function'>
        >>> f".syntax-{SyntaxRole.FUNCTION}"
        '.syntax-function'
    """

    # Control & Structure
    CONTROL_FLOW = "control"
    DECLARATION = "declaration"
    IMPORT = "import"

    # Data & Literals
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"

    # Identifiers
    TYPE = "type"
    FUNCTION = "function"
    VARIABLE = "variable"
    CONSTANT = "constant"

    # Documentation
    COMMENT = "comment"
    DOCSTRING = "docstring"

    # Feedback
    ERROR = "error"
    WARNING = "warning"
    ADDED = "added"
    REMOVED = "removed"

    # Base
    TEXT = "text"
    MUTED = "muted"

    # Additional roles
    PUNCTUATION = "punctuation"
    OPERATOR = "operator"
    ATTRIBUTE = "attribute"
    NAMESPACE = "namespace"
    TAG = "tag"
    REGEX = "regex"
    ESCAPE = "escape"
