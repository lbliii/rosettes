"""Hand-written merge conflict lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._scanners import scan_line
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["MergeStateMachineLexer"]


class MergeStateMachineLexer(StateMachineLexer):
    """Git merge conflict marker lexer."""

    name = "merge"
    aliases = ("merge-conflict", "conflict")
    filenames = ()
    mimetypes = ("text/x-merge",)

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

        while pos < length:
            content, pos, has_newline = scan_line(code, pos, length)

            if content:
                if content.startswith("<<<<<<<"):
                    token_type = TokenType.GENERIC_DELETED
                elif content.startswith("======="):
                    token_type = TokenType.GENERIC_HEADING
                elif content.startswith(">>>>>>>"):
                    token_type = TokenType.GENERIC_INSERTED
                else:
                    token_type = TokenType.TEXT

                yield Token(token_type, content, line, 1)

            if has_newline:
                col = len(content) + 1 if content else 1
                yield Token(TokenType.WHITESPACE, "\n", line, col)
                line += 1
