"""Hand-written C# lexer using composable scanner mixins.

O(n) guaranteed, zero regex, thread-safe.

**Language Support:**

- C# 12 syntax
- Attributes (`@Obsolete`, `[Attribute]`)
- Verbatim identifiers (`@class`, `@var`)
- Interpolated strings (`$"..."`), verbatim strings (`@"..."`)
- Raw string literals (triple-quoted) — C# 11
- All numeric literal formats with `_` separators

**Architecture:**

Uses C-style mixins. C#-specific additions (from Java template):

- `@` prefix: attribute → NAME_DECORATOR, verbatim identifier → NAME
- `$"..."` and `@"..."` string prefixes
- Triple-quote raw string literals

**See Also:**

- `rosettes.lexers.java_sm`: Template for @ and raw string handling
- `rosettes.lexers._scanners`: Shared mixin implementations
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import (
    IDENT_START,
    IDENT_START_DOLLAR,
    CStyleCommentsMixin,
    CStyleNumbersMixin,
    CStyleOperatorsMixin,
    CStyleStringsMixin,
    NumberConfig,
    OperatorConfig,
    StringConfig,
    scan_block_comment,
    scan_identifier,
    scan_line_comment,
    scan_string,
    scan_triple_string,
)
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["CSharpStateMachineLexer"]


_KEYWORDS: frozenset[str] = frozenset(
    {
        "abstract",
        "as",
        "base",
        "break",
        "case",
        "catch",
        "checked",
        "class",
        "const",
        "continue",
        "default",
        "delegate",
        "do",
        "else",
        "enum",
        "event",
        "explicit",
        "extern",
        "false",
        "finally",
        "fixed",
        "for",
        "foreach",
        "goto",
        "if",
        "implicit",
        "in",
        "interface",
        "internal",
        "is",
        "lock",
        "namespace",
        "new",
        "null",
        "operator",
        "out",
        "override",
        "params",
        "private",
        "protected",
        "public",
        "readonly",
        "record",
        "ref",
        "return",
        "sealed",
        "sizeof",
        "stackalloc",
        "static",
        "struct",
        "switch",
        "this",
        "throw",
        "true",
        "try",
        "typeof",
        "unchecked",
        "unsafe",
        "using",
        "var",
        "virtual",
        "void",
        "volatile",
        "while",
        "async",
        "await",
        "get",
        "set",
        "init",
        "add",
        "remove",
        "when",
        "and",
        "or",
        "not",
        "with",
        "nameof",
        "global",
    }
)

_TYPES: frozenset[str] = frozenset(
    {
        "bool",
        "byte",
        "sbyte",
        "char",
        "decimal",
        "double",
        "float",
        "int",
        "uint",
        "long",
        "ulong",
        "short",
        "ushort",
        "object",
        "string",
        "dynamic",
        "nint",
        "nuint",
    }
)

_CONSTANTS: frozenset[str] = frozenset({"true", "false", "null"})


def _scan_verbatim_string(code: str, pos: int, length: int) -> tuple[int, int]:
    """Scan C# verbatim string @"..." — "" is escaped quote.

    Args:
        code: Source code.
        pos: Position after opening ".
        length: End of code.

    Returns:
        (position after closing ", newline count).
    """
    newlines = 0
    while pos < length:
        if code[pos] == '"':
            if pos + 1 < length and code[pos + 1] == '"':
                pos += 2
                continue
            return pos + 1, newlines
        if code[pos] == "\n":
            newlines += 1
        pos += 1
    return length, newlines


class CSharpStateMachineLexer(
    CStyleCommentsMixin,
    CStyleNumbersMixin,
    CStyleStringsMixin,
    CStyleOperatorsMixin,
    StateMachineLexer,
):
    """C# lexer using composable mixins."""

    name = "csharp"
    aliases = ("cs", "c#")
    filenames = ("*.cs", "*.csx")
    mimetypes = ("text/x-csharp",)

    NUMBER_CONFIG = NumberConfig(
        integer_suffixes=("u", "U", "l", "L", "ul", "UL", "lu", "LU"),
        float_suffixes=("f", "F", "d", "D", "m", "M"),
    )

    STRING_CONFIG = StringConfig(
        single_quote=True,
        double_quote=True,
        backtick=False,
    )

    OPERATOR_CONFIG = OperatorConfig(
        three_char=frozenset({"...", ">>=", "<<=", "??="}),
        two_char=frozenset(
            {
                "->",
                "=>",
                "++",
                "--",
                "&&",
                "||",
                "==",
                "!=",
                "<=",
                ">=",
                "<<",
                ">>",
                "+=",
                "-=",
                "*=",
                "/=",
                "%=",
                "&=",
                "|=",
                "^=",
                "??",
                "?.",
                "?[",
            }
        ),
        one_char=frozenset("+-*/%&|^!~<>=?:"),
    )

    def tokenize(
        self,
        code: str,
        config: LexerConfig | None = None,
        *,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]:
        pos = start
        length = end if end is not None else len(code)
        line = 1
        line_start = start

        while pos < length:
            char = code[pos]
            col = pos - line_start + 1

            # Whitespace
            if char in self.WHITESPACE:
                start_pos = pos
                start_line = line
                while pos < length and code[pos] in self.WHITESPACE:
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                    pos += 1
                yield Token(TokenType.WHITESPACE, code[start_pos:pos], start_line, col)
                continue

            # Comments (including /// doc comments)
            if char == "/" and pos + 1 < length:
                next_char = code[pos + 1]
                if next_char == "/":
                    start_pos = pos
                    pos = scan_line_comment(code, pos + 2)
                    yield Token(TokenType.COMMENT_SINGLE, code[start_pos:pos], line, col)
                    continue
                if next_char == "*":
                    start_pos = pos
                    is_doc = pos + 2 < length and code[pos + 2] == "*"
                    pos = scan_block_comment(code, pos + 2, "*/")
                    value = code[start_pos:pos]
                    newlines = value.count("\n")
                    token_type = TokenType.STRING_DOC if is_doc else TokenType.COMMENT_MULTILINE
                    yield Token(token_type, value, line, col)
                    if newlines:
                        line += newlines
                        line_start = start_pos + value.rfind("\n") + 1
                    continue

            # $"..." interpolated or $@"..." verbatim interpolated (before @)
            if char == "$" and pos + 1 < length:
                next_char = code[pos + 1]
                if next_char == "@" and pos + 2 < length and code[pos + 2] == '"':
                    start_pos = pos
                    pos += 3
                    pos, newlines = _scan_verbatim_string(code, pos, length)
                    yield Token(TokenType.STRING, code[start_pos:pos], line, col)
                    if newlines:
                        line += newlines
                        line_start = start_pos + code[start_pos:pos].rfind("\n") + 1
                    continue
                if next_char == '"':
                    start_pos = pos
                    pos += 2
                    pos, newlines = scan_string(code, pos, '"')
                    yield Token(TokenType.STRING, code[start_pos:pos], line, col)
                    if newlines:
                        line += newlines
                        line_start = start_pos + code[start_pos:pos].rfind("\n") + 1
                    continue

            # @"..." verbatim string (must be before @ prefix)
            if char == "@" and pos + 1 < length and code[pos + 1] == '"':
                start_pos = pos
                pos += 2
                pos, newlines = _scan_verbatim_string(code, pos, length)
                yield Token(TokenType.STRING, code[start_pos:pos], line, col)
                if newlines:
                    line += newlines
                    line_start = start_pos + code[start_pos:pos].rfind("\n") + 1
                continue

            # @ prefix (attribute or verbatim identifier)
            if char == "@":
                start_pos = pos
                pos += 1
                if pos < length and code[pos] in IDENT_START_DOLLAR:
                    pos = scan_identifier(code, pos, allow_dollar=True)
                    word = code[start_pos + 1 : pos]
                    if word in _KEYWORDS or word in _TYPES:
                        yield Token(TokenType.NAME, code[start_pos:pos], line, col)
                    else:
                        yield Token(TokenType.NAME_DECORATOR, code[start_pos:pos], line, col)
                else:
                    yield Token(TokenType.NAME_DECORATOR, code[start_pos:pos], line, col)
                continue

            # """ raw string (C# 11)
            if char == '"' and pos + 2 < length and code[pos : pos + 3] == '"""':
                start_pos = pos
                pos += 3
                pos, newlines = scan_triple_string(code, pos, '"')
                yield Token(TokenType.STRING_DOC, code[start_pos:pos], line, col)
                if newlines:
                    line += newlines
                    line_start = start_pos + code[start_pos:pos].rfind("\n") + 1
                continue

            # Regular strings (use mixin)
            token, new_pos, newlines = self._try_string(code, pos, line, col)
            if token:
                yield token
                pos = new_pos
                if newlines:
                    line += newlines
                    line_start = pos - len(token.value) + token.value.rfind("\n") + 1
                continue

            # Character literals
            if char == "'":
                start_pos = pos
                pos += 1
                pos, _ = scan_string(code, pos, "'")
                yield Token(TokenType.STRING_CHAR, code[start_pos:pos], line, col)
                continue

            # Numbers
            token, new_pos = self._try_number(code, pos, line, col)
            if token:
                yield token
                pos = new_pos
                continue

            # Identifiers
            if char in IDENT_START:
                start_pos = pos
                pos = scan_identifier(code, pos)
                word = code[start_pos:pos]
                token_type = self._classify_word(word)
                yield Token(token_type, word, line, col)
                continue

            # Operators
            token, new_pos = self._try_operator(code, pos, line, col)
            if token:
                yield token
                pos = new_pos
                continue

            # Punctuation
            if char in "()[]{}:;,.":
                yield Token(TokenType.PUNCTUATION, char, line, col)
                pos += 1
                continue

            yield Token(TokenType.ERROR, char, line, col)
            pos += 1

    def _classify_word(self, word: str) -> TokenType:
        if word in _CONSTANTS:
            return TokenType.KEYWORD_CONSTANT
        if word in ("class", "interface", "enum", "record", "struct", "delegate"):
            return TokenType.KEYWORD_DECLARATION
        if word in ("namespace", "using"):
            return TokenType.KEYWORD_NAMESPACE
        if word in _KEYWORDS:
            return TokenType.KEYWORD
        if word in _TYPES:
            return TokenType.KEYWORD_TYPE
        if word and word[0].isupper():
            return TokenType.NAME_CLASS
        return TokenType.NAME
