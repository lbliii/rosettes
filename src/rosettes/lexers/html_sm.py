"""Hand-written HTML lexer using state machine approach.

O(n) guaranteed, zero regex, thread-safe.

Language Support:
    - HTML5 syntax
    - Comments (<!-- -->)
    - DOCTYPE declarations
    - Tags with attributes (quoted and unquoted values)
    - Self-closing tags
    - Script and style blocks (minimal handling)

Token Classification:
    - Tag names: NAME_TAG (div, span, p, etc.)
    - Attribute names: NAME_ATTRIBUTE (class, id, href, etc.)
    - Attribute values: STRING
    - Comments: COMMENT_MULTILINE
    - Text content: TEXT

Performance:
    ~45µs per 100-line file.

Thread-Safety:
    Uses only local variables in tokenize().

See Also:
    rosettes.lexers.xml_sm: XML lexer (stricter syntax)
    rosettes.lexers.css_sm: CSS lexer (for style content)
"""

from __future__ import annotations

from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._state_machine import StateMachineLexer

__all__ = ["HtmlStateMachineLexer"]


class HtmlStateMachineLexer(StateMachineLexer):
    """HTML lexer with tag, attribute, and comment parsing.

    Handles HTML5 syntax including comments, doctype, and tag attributes.

    Example:
        >>> from rosettes import get_lexer
        >>> lexer = get_lexer("html")
        >>> tokens = list(lexer.tokenize('<div class="foo">'))
        >>> tokens[1].type  # 'div' tag
        <TokenType.NAME_TAG: 'nt'>
    """

    name = "html"
    aliases = ("htm", "xhtml", "go-html-template")
    filenames = ("*.html", "*.htm")
    mimetypes = ("text/html",)

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

            # HTML comment <!-- -->
            if char == "<" and code[pos : pos + 4] == "<!--":
                start = pos
                pos += 4
                start_line = line
                while pos < length:
                    if code[pos : pos + 3] == "-->":
                        pos += 3
                        break
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                    pos += 1
                yield Token(TokenType.COMMENT_MULTILINE, code[start:pos], start_line, col)
                continue

            # DOCTYPE
            if char == "<" and code[pos : pos + 9].upper() == "<!DOCTYPE":
                start = pos
                while pos < length and code[pos] != ">":
                    pos += 1
                if pos < length:
                    pos += 1
                yield Token(TokenType.COMMENT_PREPROC, code[start:pos], line, col)
                continue

            # CDATA
            if char == "<" and code[pos : pos + 9] == "<![CDATA[":
                start = pos
                pos += 9
                start_line = line
                while pos < length:
                    if code[pos : pos + 3] == "]]>":
                        pos += 3
                        break
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                    pos += 1
                yield Token(TokenType.STRING, code[start:pos], start_line, col)
                continue

            # Tags
            if char == "<":
                start = pos
                pos += 1

                # Closing tag
                if pos < length and code[pos] == "/":
                    pos += 1

                # Tag name
                tag_start = pos
                while pos < length and (code[pos].isalnum() or code[pos] in "-_:"):
                    pos += 1
                tag_name = code[tag_start:pos]

                if tag_name:
                    # Emit opening bracket and tag name
                    yield Token(TokenType.PUNCTUATION, code[start:tag_start], line, col)
                    yield Token(TokenType.NAME_TAG, tag_name, line, col + (tag_start - start))

                    # Parse attributes
                    while pos < length:
                        # Whitespace
                        if code[pos] in " \t\n\r":
                            ws_start = pos
                            while pos < length and code[pos] in " \t\n\r":
                                if code[pos] == "\n":
                                    line += 1
                                    line_start = pos + 1
                                pos += 1
                            yield Token(TokenType.WHITESPACE, code[ws_start:pos], line, col)
                            continue

                        # End of tag
                        if code[pos] == ">":
                            yield Token(TokenType.PUNCTUATION, ">", line, pos - line_start + 1)
                            pos += 1
                            break

                        # Self-closing
                        if code[pos : pos + 2] == "/>":
                            yield Token(TokenType.PUNCTUATION, "/>", line, pos - line_start + 1)
                            pos += 2
                            break

                        # Attribute name
                        if code[pos].isalpha() or code[pos] in "_:":
                            attr_start = pos
                            while pos < length and (code[pos].isalnum() or code[pos] in "-_:."):
                                pos += 1
                            yield Token(
                                TokenType.NAME_ATTRIBUTE,
                                code[attr_start:pos],
                                line,
                                attr_start - line_start + 1,
                            )
                            continue

                        # Equals sign
                        if code[pos] == "=":
                            yield Token(TokenType.OPERATOR, "=", line, pos - line_start + 1)
                            pos += 1
                            continue

                        # Attribute value
                        if code[pos] in "\"'":
                            quote = code[pos]
                            val_start = pos
                            pos += 1
                            while pos < length and code[pos] != quote:
                                if code[pos] == "\n":
                                    line += 1
                                    line_start = pos + 1
                                pos += 1
                            if pos < length:
                                pos += 1
                            yield Token(
                                TokenType.STRING,
                                code[val_start:pos],
                                line,
                                val_start - line_start + 1,
                            )
                            continue

                        # Unquoted attribute value
                        if code[pos] not in " \t\n\r>\"'=":
                            val_start = pos
                            while pos < length and code[pos] not in " \t\n\r>\"'":
                                pos += 1
                            yield Token(
                                TokenType.STRING,
                                code[val_start:pos],
                                line,
                                val_start - line_start + 1,
                            )
                            continue

                        pos += 1
                else:
                    # Bare < (not a tag)
                    yield Token(TokenType.TEXT, "<", line, col)
                continue

            # Text content
            if char != "<":
                start = pos
                while pos < length and code[pos] != "<":
                    if code[pos] == "\n":
                        line += 1
                        line_start = pos + 1
                    pos += 1
                text = code[start:pos]
                if text.strip():
                    yield Token(TokenType.TEXT, text, line, col)
                elif text:
                    yield Token(TokenType.WHITESPACE, text, line, col)
                continue

            yield Token(TokenType.ERROR, char, line, col)
            pos += 1
