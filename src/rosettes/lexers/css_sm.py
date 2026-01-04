"""Hand-written CSS lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.

Language Support:
    - CSS3 syntax
    - Selectors (class, id, element, pseudo, attribute)
    - Properties and values
    - At-rules (@media, @import, @keyframes, etc.)
    - CSS custom properties (--var-name)
    - Color formats (#hex, rgb(), hsl(), etc.)
    - calc() and other functions
    - Comments (/* */)

Token Classification:
    - Selectors: .class → NAME_CLASS, #id → NAME_FUNCTION
    - Properties: color, font-size → NAME_PROPERTY
    - Values: blue, 12px, #fff → various (STRING, NUMBER, etc.)
    - At-rules: @media → NAME_DECORATOR
    - Variables: --custom-prop → NAME_VARIABLE

Performance:
    ~50µs per 100-line file.

Thread-Safety:
    Uses only local variables in tokenize().

See Also:
    rosettes.lexers.html_sm: HTML lexer (CSS in style tags)
    rosettes.lexers.scss_sm: SCSS lexer (CSS preprocessor)
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import (
    DIGITS,
    HEX_DIGITS,
    scan_block_comment,
    scan_string,
)
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["CssStateMachineLexer"]


class CssStateMachineLexer(StateMachineLexer):
    """CSS lexer with selector, property, and value parsing.

    Handles CSS3 syntax including at-rules, custom properties, and functions.

    Example:
        >>> from rosettes import get_lexer
        >>> lexer = get_lexer("css")
        >>> tokens = list(lexer.tokenize(".btn { color: red; }"))
        >>> tokens[0].type  # '.btn' class selector
        <TokenType.NAME_CLASS: 'nc'>
    """

    name = "css"
    aliases = ("css3",)
    filenames = ("*.css",)
    mimetypes = ("text/css",)

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
                start = pos
                start_line = line
                while pos < length and code[pos] in self.WHITESPACE:
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                    pos += 1
                yield Token(TokenType.WHITESPACE, code[start:pos], start_line, col)
                continue

            # Comments /* */
            if char == "/" and pos + 1 < length and code[pos + 1] == "*":
                start = pos
                pos = scan_block_comment(code, pos + 2, "*/")
                value = code[start:pos]
                newlines = value.count("\n")
                yield Token(TokenType.COMMENT_MULTILINE, value, line, col)
                if newlines:
                    line += newlines
                    line_start = start + value.rfind("\n") + 1
                continue

            # At-rules @media, @import, etc.
            if char == "@":
                start = pos
                pos += 1
                while pos < length and (code[pos].isalnum() or code[pos] in "-_"):
                    pos += 1
                yield Token(TokenType.KEYWORD, code[start:pos], line, col)
                continue

            # ID selectors #id
            if char == "#":
                start = pos
                pos += 1
                # Could be hex color or ID
                hex_start = pos
                while pos < length and code[pos] in HEX_DIGITS:
                    pos += 1
                hex_len = pos - hex_start
                if hex_len in (3, 4, 6, 8) and (pos >= length or not code[pos].isalnum()):
                    # It's a color
                    yield Token(TokenType.NUMBER_HEX, code[start:pos], line, col)
                else:
                    # It's an ID selector
                    while pos < length and (code[pos].isalnum() or code[pos] in "-_"):
                        pos += 1
                    yield Token(TokenType.NAME_TAG, code[start:pos], line, col)
                continue

            # Class selectors .class
            if char == ".":
                if pos + 1 < length and (code[pos + 1].isalpha() or code[pos + 1] in "-_"):
                    start = pos
                    pos += 1
                    while pos < length and (code[pos].isalnum() or code[pos] in "-_"):
                        pos += 1
                    yield Token(TokenType.NAME_CLASS, code[start:pos], line, col)
                    continue
                # Could be a number starting with .
                if pos + 1 < length and code[pos + 1] in DIGITS:
                    start = pos
                    pos += 1
                    while pos < length and code[pos] in DIGITS:
                        pos += 1
                    yield Token(TokenType.NUMBER_FLOAT, code[start:pos], line, col)
                    continue
                yield Token(TokenType.PUNCTUATION, ".", line, col)
                pos += 1
                continue

            # Strings
            if char in "\"'":
                start = pos
                quote = char
                pos += 1
                pos, _ = scan_string(code, pos, quote)
                yield Token(TokenType.STRING, code[start:pos], line, col)
                continue

            # Numbers (including units)
            if char in DIGITS or (char == "-" and pos + 1 < length and code[pos + 1] in DIGITS):
                start = pos
                if char == "-":
                    pos += 1
                while pos < length and code[pos] in DIGITS:
                    pos += 1
                if pos < length and code[pos] == ".":
                    pos += 1
                    while pos < length and code[pos] in DIGITS:
                        pos += 1
                # Unit suffix
                unit_start = pos
                while (
                    pos < length
                    and code[pos] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%"
                ):
                    pos += 1
                yield Token(
                    TokenType.NUMBER_FLOAT
                    if "." in code[start:unit_start]
                    else TokenType.NUMBER_INTEGER,
                    code[start:pos],
                    line,
                    col,
                )
                continue

            # Property names and values (identifiers)
            if char.isalpha() or char in "-_":
                start = pos
                while pos < length and (code[pos].isalnum() or code[pos] in "-_"):
                    pos += 1
                word = code[start:pos]
                # Check if it's a property (followed by :) or value
                temp = pos
                while temp < length and code[temp] in " \t":
                    temp += 1
                if temp < length and code[temp] == ":":
                    yield Token(TokenType.NAME_ATTRIBUTE, word, line, col)
                else:
                    yield Token(TokenType.NAME, word, line, col)
                continue

            # Pseudo-classes and pseudo-elements
            if char == ":":
                start = pos
                pos += 1
                if pos < length and code[pos] == ":":
                    pos += 1  # ::pseudo-element
                while pos < length and (code[pos].isalnum() or code[pos] in "-_"):
                    pos += 1
                if pos > start + 1:
                    yield Token(TokenType.NAME_DECORATOR, code[start:pos], line, col)
                else:
                    yield Token(TokenType.PUNCTUATION, ":", line, col)
                continue

            # Important
            if char == "!" and pos + 9 <= length and code[pos : pos + 10].lower() == "!important":
                yield Token(TokenType.KEYWORD, "!important", line, col)
                pos += 10
                continue

            # Operators
            if char in "+>~*":
                yield Token(TokenType.OPERATOR, char, line, col)
                pos += 1
                continue

            # Attribute selectors [attr]
            if char == "[":
                start = pos
                bracket_depth = 1
                pos += 1
                while pos < length and bracket_depth > 0:
                    if code[pos] == "[":
                        bracket_depth += 1
                    elif code[pos] == "]":
                        bracket_depth -= 1
                    pos += 1
                yield Token(TokenType.NAME_ATTRIBUTE, code[start:pos], line, col)
                continue

            # Punctuation
            if char in "{}();,":
                yield Token(TokenType.PUNCTUATION, char, line, col)
                pos += 1
                continue

            yield Token(TokenType.ERROR, char, line, col)
            pos += 1
