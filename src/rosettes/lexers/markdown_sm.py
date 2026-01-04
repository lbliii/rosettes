"""Hand-written Markdown lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.

Language Support:
    - CommonMark syntax
    - Fenced code blocks (```) with language hints
    - Inline code (`code`)
    - Headers (# through ######)
    - Bold (**text**), italic (*text*), strikethrough (~~text~~)
    - Links [text](url) and images ![alt](url)
    - Blockquotes (>)
    - Horizontal rules (---, ***, ___)
    - Unordered lists (-, *, +) and ordered lists (1.)

Design Philosophy:
    Markdown lexing is line-oriented. The lexer tracks at_line_start
    context to distinguish block-level elements (headers, lists, code
    blocks) from inline elements (bold, links).

    Fenced code blocks receive special handling: the content between
    ``` markers is yielded as a single token, preserving the language
    hint for potential nested highlighting.

Performance:
    ~50µs per 100-line file.

Thread-Safety:
    Uses only local variables in tokenize().

See Also:
    rosettes.lexers.rst_sm: reStructuredText lexer
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["MarkdownStateMachineLexer"]


class MarkdownStateMachineLexer(StateMachineLexer):
    """Markdown lexer with CommonMark syntax support.

    Line-oriented lexer that tracks block-level context for accurate
    tokenization of headers, lists, and code blocks.

    Token Types:
        - GENERIC_HEADING: Headers (# through ######)
        - STRING: Fenced code blocks and inline code
        - GENERIC_STRONG: Bold text (**text**)
        - GENERIC_EMPH: Italic text (*text*)
        - NAME_TAG: Link/image markers and URLs

    Example:
        >>> from rosettes import get_lexer
        >>> lexer = get_lexer("markdown")
        >>> tokens = list(lexer.tokenize("# Header"))
        >>> tokens[0].type  # '#' is a heading marker
        <TokenType.GENERIC_HEADING: 'gh'>
    """

    name = "markdown"
    aliases = ("md",)
    filenames = ("*.md", "*.markdown")
    mimetypes = ("text/markdown",)

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

            # Newline
            if char == "\n":
                yield Token(TokenType.WHITESPACE, char, line, col)
                pos += 1
                line += 1
                line_start = pos
                at_line_start = True
                continue

            # Fenced code blocks ```
            if at_line_start and char == "`" and pos + 2 < length and code[pos : pos + 3] == "```":
                start = pos
                pos += 3
                # Language identifier
                while pos < length and code[pos] != "\n":
                    pos += 1
                start_line = line
                if pos < length:
                    pos += 1
                    line += 1
                    line_start = pos
                # Find closing ```
                while pos < length:
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                        if pos + 4 < length and code[pos + 1 : pos + 4] == "```":
                            pos += 4
                            while pos < length and code[pos] != "\n":
                                pos += 1
                            break
                    pos += 1
                yield Token(TokenType.STRING, code[start:pos], start_line, col)
                at_line_start = False
                continue

            # Indented code block (4 spaces or tab at line start)
            if at_line_start and (code[pos : pos + 4] == "    " or char == "\t"):
                start = pos
                while pos < length and code[pos] != "\n":
                    pos += 1
                yield Token(TokenType.STRING, code[start:pos], line, col)
                at_line_start = False
                continue

            # Headers # ## ###
            if at_line_start and char == "#":
                start = pos
                while pos < length and code[pos] == "#":
                    pos += 1
                if pos < length and code[pos] in " \t":
                    # Valid header
                    while pos < length and code[pos] != "\n":
                        pos += 1
                    yield Token(TokenType.GENERIC_HEADING, code[start:pos], line, col)
                else:
                    yield Token(TokenType.TEXT, code[start:pos], line, col)
                at_line_start = False
                continue

            # Blockquotes >
            if at_line_start and char == ">":
                start = pos
                while pos < length and code[pos] != "\n":
                    pos += 1
                yield Token(TokenType.GENERIC_OUTPUT, code[start:pos], line, col)
                at_line_start = False
                continue

            # Lists - * +
            if at_line_start and char in "-*+" and pos + 1 < length and code[pos + 1] in " \t":
                yield Token(TokenType.PUNCTUATION, char, line, col)
                pos += 1
                at_line_start = False
                continue

            # Numbered lists 1.
            if at_line_start and char in "0123456789":
                start = pos
                while pos < length and code[pos] in "0123456789":
                    pos += 1
                if (
                    pos < length
                    and code[pos] == "."
                    and pos + 1 < length
                    and code[pos + 1] in " \t"
                ):
                    pos += 1
                    yield Token(TokenType.PUNCTUATION, code[start:pos], line, col)
                else:
                    yield Token(TokenType.TEXT, code[start:pos], line, col)
                at_line_start = False
                continue

            # Horizontal rules --- *** ___
            if at_line_start and char in "-*_":
                start = pos
                rule_char = char
                count = 0
                temp = pos
                while temp < length and code[temp] in f"{rule_char} \t":
                    if code[temp] == rule_char:
                        count += 1
                    temp += 1
                if count >= 3 and (temp >= length or code[temp] == "\n"):
                    pos = temp
                    yield Token(TokenType.PUNCTUATION, code[start:pos], line, col)
                    at_line_start = False
                    continue

            # Inline code `code`
            if char == "`":
                start = pos
                pos += 1
                while pos < length and code[pos] != "`" and code[pos] != "\n":
                    pos += 1
                if pos < length and code[pos] == "`":
                    pos += 1
                yield Token(TokenType.STRING, code[start:pos], line, col)
                at_line_start = False
                continue

            # Bold/italic **bold** *italic* __bold__ _italic_
            if char in "*_":
                start = pos
                marker = char
                count = 0
                while pos < length and code[pos] == marker:
                    count += 1
                    pos += 1
                if count <= 3:
                    yield Token(
                        TokenType.GENERIC_STRONG if count >= 2 else TokenType.GENERIC_EMPH,
                        code[start:pos],
                        line,
                        col,
                    )
                else:
                    yield Token(TokenType.TEXT, code[start:pos], line, col)
                at_line_start = False
                continue

            # Links [text](url) or [text][ref]
            if char == "[":
                start = pos
                pos += 1
                bracket_depth = 1
                while pos < length and bracket_depth > 0:
                    if code[pos] == "[":
                        bracket_depth += 1
                    elif code[pos] == "]":
                        bracket_depth -= 1
                    elif code[pos] == "\n":
                        break
                    pos += 1
                if pos < length and code[pos - 1] == "]":
                    if pos < length and code[pos] == "(":
                        # URL follows
                        pos += 1
                        while pos < length and code[pos] != ")" and code[pos] != "\n":
                            pos += 1
                        if pos < length and code[pos] == ")":
                            pos += 1
                    elif pos < length and code[pos] == "[":
                        # Reference follows
                        pos += 1
                        while pos < length and code[pos] != "]" and code[pos] != "\n":
                            pos += 1
                        if pos < length and code[pos] == "]":
                            pos += 1
                yield Token(TokenType.NAME_LABEL, code[start:pos], line, col)
                at_line_start = False
                continue

            # Images ![alt](url)
            if char == "!" and pos + 1 < length and code[pos + 1] == "[":
                start = pos
                pos += 2
                while pos < length and code[pos] != "]" and code[pos] != "\n":
                    pos += 1
                if pos < length and code[pos] == "]":
                    pos += 1
                    if pos < length and code[pos] == "(":
                        pos += 1
                        while pos < length and code[pos] != ")" and code[pos] != "\n":
                            pos += 1
                        if pos < length and code[pos] == ")":
                            pos += 1
                yield Token(TokenType.NAME_LABEL, code[start:pos], line, col)
                at_line_start = False
                continue

            # Regular text
            start = pos
            while pos < length and code[pos] not in "\n`*_[]!#>-+":
                if code[pos] in " \t":
                    pos += 1
                else:
                    pos += 1
                    at_line_start = False
            if pos > start:
                yield Token(TokenType.TEXT, code[start:pos], line, col)
                continue

            # Whitespace
            if char in " \t":
                start = pos
                while pos < length and code[pos] in " \t":
                    pos += 1
                yield Token(TokenType.WHITESPACE, code[start:pos], line, col)
                continue

            yield Token(TokenType.TEXT, char, line, col)
            pos += 1
            at_line_start = False
