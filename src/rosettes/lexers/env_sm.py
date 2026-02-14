"""Hand-written .env lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import scan_line_comment, scan_string
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["EnvStateMachineLexer"]


class EnvStateMachineLexer(StateMachineLexer):
    """Environment variable file (.env) lexer."""

    name = "env"
    aliases = ("dotenv", ".env")
    filenames = (".env", "*.env", ".env.local", ".env.example")
    mimetypes = ("text/x-env",)

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
        at_line_start = True

        while pos < length:
            char = code[pos]
            col = pos - line_start + 1

            # Whitespace
            if char in " \t":
                start_pos = pos
                while pos < length and code[pos] in " \t":
                    pos += 1
                yield Token(TokenType.WHITESPACE, code[start_pos:pos], line, col)
                continue

            if char == "\n":
                yield Token(TokenType.WHITESPACE, char, line, col)
                pos += 1
                line += 1
                line_start = pos
                at_line_start = True
                continue

            # Comments (#)
            if char == "#":
                start_pos = pos
                pos = scan_line_comment(code, pos + 1)
                yield Token(TokenType.COMMENT_SINGLE, code[start_pos:pos], line, col)
                at_line_start = False
                continue

            # Optional export prefix (at line start)
            if at_line_start and pos + 6 < length and code[pos : pos + 7] == "export ":
                yield Token(TokenType.KEYWORD, "export ", line, col)
                pos += 7
                at_line_start = False
                continue

            # Keys (before =)
            if at_line_start and (char.isalpha() or char in "_-"):
                start_pos = pos
                while pos < length and code[pos] not in "=\n#":
                    pos += 1
                key = code[start_pos:pos].rstrip()
                if key:
                    yield Token(TokenType.NAME_ATTRIBUTE, key, line, col)
                    pos = start_pos + len(key)
                at_line_start = False
                continue

            # Assignment operator
            if char == "=":
                yield Token(TokenType.OPERATOR, char, line, col)
                pos += 1
                at_line_start = False
                continue

            # Quoted values
            if char in "\"'":
                start_pos = pos
                quote = char
                pos += 1
                pos, _ = scan_string(code, pos, quote)
                yield Token(TokenType.STRING, code[start_pos:pos], line, col)
                at_line_start = False
                continue

            # Unquoted value (rest of line, no #)
            if char not in "\n#":
                start_pos = pos
                while pos < length and code[pos] not in "\n#":
                    pos += 1
                value = code[start_pos:pos].rstrip()
                if value:
                    yield Token(TokenType.STRING, value, line, col)
                    pos = start_pos + len(value)
                at_line_start = False
                continue

            yield Token(TokenType.TEXT, char, line, col)
            pos += 1
            at_line_start = False
