"""Hand-written HTTP request/response lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import scan_line
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["HttpStateMachineLexer"]

_HTTP_METHODS: frozenset[str] = frozenset(
    {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "CONNECT", "TRACE"}
)


class HttpStateMachineLexer(StateMachineLexer):
    """HTTP request/response lexer."""

    name = "http"
    aliases = ("http-request", "http-response")
    filenames = ()
    mimetypes = ("message/http",)

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
        in_body = False

        while pos < length:
            content, pos, has_newline = scan_line(code, pos, length)

            if content:
                if not in_body:
                    # Request/status line (GET /path HTTP/1.1 or HTTP/1.1 200 OK)
                    first_word = content.split(None, 1)[0] if content.split() else ""
                    if first_word in _HTTP_METHODS or first_word.startswith("HTTP/"):
                        yield Token(TokenType.GENERIC_HEADING, content, line, 1)
                    elif ": " in content:
                        # Header line
                        colon_idx = content.find(": ")
                        yield Token(
                            TokenType.NAME_ATTRIBUTE,
                            content[:colon_idx],
                            line,
                            1,
                        )
                        yield Token(TokenType.OPERATOR, ": ", line, colon_idx + 1)
                        yield Token(
                            TokenType.STRING,
                            content[colon_idx + 2 :],
                            line,
                            colon_idx + 3,
                        )
                    else:
                        # Blank line starts body
                        if content.strip() == "":
                            in_body = True
                            yield Token(TokenType.WHITESPACE, content, line, 1)
                        else:
                            yield Token(TokenType.TEXT, content, line, 1)
                else:
                    yield Token(TokenType.TEXT, content, line, 1)
            else:
                # Empty line
                if has_newline:
                    if not in_body and pos < length:
                        in_body = True
                    yield Token(TokenType.WHITESPACE, "\n", line, 1)

            if has_newline:
                col = len(content) + 1 if content else 1
                if content:
                    yield Token(TokenType.WHITESPACE, "\n", line, col)
                line += 1
