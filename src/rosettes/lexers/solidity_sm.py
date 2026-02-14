"""Hand-written Solidity lexer using composable scanner mixins.

O(n) guaranteed, zero regex, thread-safe.

**Language Support:**

- Solidity 0.8.x syntax
- NatSpec comments (`///` and `/**`)
- Contract, interface, library, function, mapping, event
- All standard types (address, uint, int, bool, etc.)

**Architecture:**

Uses C-style mixins. Solidity-specific additions (from C template):

- `///` NatSpec line comments
- `=>` for function types (from C++ OperatorConfig)
- Contract-specific keywords and types

**See Also:**

- `rosettes.lexers.c_sm`: Template for C-style tokenize loop
- `rosettes.lexers._scanners`: Shared mixin implementations
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import (
    IDENT_START,
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
)
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["SolidityStateMachineLexer"]


_KEYWORDS: frozenset[str] = frozenset(
    {
        "abstract",
        "anonymous",
        "as",
        "assembly",
        "break",
        "calldata",
        "catch",
        "constant",
        "constructor",
        "continue",
        "contract",
        "delete",
        "do",
        "else",
        "emit",
        "enum",
        "error",
        "event",
        "external",
        "fallback",
        "for",
        "function",
        "if",
        "immutable",
        "import",
        "indexed",
        "interface",
        "internal",
        "library",
        "mapping",
        "memory",
        "modifier",
        "new",
        "override",
        "payable",
        "pragma",
        "private",
        "public",
        "receive",
        "return",
        "returns",
        "revert",
        "storage",
        "struct",
        "try",
        "typeof",
        "unchecked",
        "using",
        "view",
        "virtual",
        "while",
    }
)

_TYPES: frozenset[str] = frozenset(
    {
        "address",
        "bool",
        "bytes",
        "string",
        "uint",
        "int",
        "uint8",
        "uint16",
        "uint24",
        "uint32",
        "uint40",
        "uint48",
        "uint56",
        "uint64",
        "uint72",
        "uint80",
        "uint88",
        "uint96",
        "uint104",
        "uint112",
        "uint120",
        "uint128",
        "uint136",
        "uint144",
        "uint152",
        "uint160",
        "uint168",
        "uint176",
        "uint184",
        "uint192",
        "uint200",
        "uint208",
        "uint216",
        "uint224",
        "uint232",
        "uint240",
        "uint248",
        "uint256",
        "int8",
        "int16",
        "int24",
        "int32",
        "int40",
        "int48",
        "int56",
        "int64",
        "int72",
        "int80",
        "int88",
        "int96",
        "int104",
        "int112",
        "int120",
        "int128",
        "int136",
        "int144",
        "int152",
        "int160",
        "int168",
        "int176",
        "int184",
        "int192",
        "int200",
        "int208",
        "int216",
        "int224",
        "int232",
        "int240",
        "int248",
        "int256",
        "fixed",
        "ufixed",
        "byte",
    }
)

_CONSTANTS: frozenset[str] = frozenset({"true", "false"})


class SolidityStateMachineLexer(
    CStyleCommentsMixin,
    CStyleNumbersMixin,
    CStyleStringsMixin,
    CStyleOperatorsMixin,
    StateMachineLexer,
):
    """Solidity lexer using composable mixins."""

    name = "solidity"
    aliases = ("sol",)
    filenames = ("*.sol",)
    mimetypes = ("text/x-solidity",)

    NUMBER_CONFIG = NumberConfig(
        integer_suffixes=(),
        float_suffixes=(),
    )

    STRING_CONFIG = StringConfig(
        single_quote=True,
        double_quote=True,
        backtick=False,
    )

    OPERATOR_CONFIG = OperatorConfig(
        three_char=frozenset({"...", ">>=", "<<="}),
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

            # Comments: /// NatSpec or // line comment
            if char == "/" and pos + 1 < length:
                next_char = code[pos + 1]
                if next_char == "/":
                    start_pos = pos
                    pos = scan_line_comment(code, pos + 2)
                    yield Token(TokenType.COMMENT_SINGLE, code[start_pos:pos], line, col)
                    continue
                if next_char == "*":
                    start_pos = pos
                    is_natspec = pos + 2 < length and code[pos + 2] == "*"
                    pos = scan_block_comment(code, pos + 2, "*/")
                    value = code[start_pos:pos]
                    newlines = value.count("\n")
                    token_type = TokenType.STRING_DOC if is_natspec else TokenType.COMMENT_MULTILINE
                    yield Token(token_type, value, line, col)
                    if newlines:
                        line += newlines
                        line_start = start_pos + value.rfind("\n") + 1
                    continue

            # Strings
            token, new_pos, newlines = self._try_string(code, pos, line, col)
            if token:
                yield token
                pos = new_pos
                if newlines:
                    line += newlines
                    line_start = pos - len(token.value) + token.value.rfind("\n") + 1
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
        if word in ("contract", "interface", "library", "enum", "struct", "function", "event"):
            return TokenType.KEYWORD_DECLARATION
        if word in ("import", "using", "pragma"):
            return TokenType.KEYWORD_NAMESPACE
        if word in _KEYWORDS:
            return TokenType.KEYWORD
        if word in _TYPES:
            return TokenType.KEYWORD_TYPE
        if word and word[0].isupper():
            return TokenType.NAME_CLASS
        return TokenType.NAME
