"""Edge-case tests for format lexers (env, http, merge)."""

from __future__ import annotations

from rosettes import TokenType, get_lexer


class TestEnvLexer:
    """Edge cases for .env lexer."""

    def test_empty_input(self) -> None:
        lexer = get_lexer("env")
        tokens = list(lexer.tokenize(""))
        assert tokens == []

    def test_single_key_value_reconstructs(self) -> None:
        lexer = get_lexer("env")
        code = "KEY=value"
        tokens = list(lexer.tokenize(code))
        assert "".join(t.value for t in tokens) == code

    def test_export_prefix(self) -> None:
        lexer = get_lexer("env")
        code = "export FOO=bar"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.KEYWORD in types
        assert "".join(t.value for t in tokens) == code

    def test_empty_value(self) -> None:
        lexer = get_lexer("env")
        code = "EMPTY="
        tokens = list(lexer.tokenize(code))
        assert "".join(t.value for t in tokens) == code

    def test_comment_only(self) -> None:
        lexer = get_lexer("env")
        code = "# comment"
        tokens = list(lexer.tokenize(code))
        assert any(t.type == TokenType.COMMENT_SINGLE for t in tokens)
        assert "".join(t.value for t in tokens) == code


class TestHttpLexer:
    """Edge cases for HTTP lexer."""

    def test_empty_input(self) -> None:
        lexer = get_lexer("http")
        tokens = list(lexer.tokenize(""))
        assert tokens == []

    def test_request_line_only(self) -> None:
        lexer = get_lexer("http")
        code = "GET / HTTP/1.1"
        tokens = list(lexer.tokenize(code))
        assert any(t.type == TokenType.GENERIC_HEADING for t in tokens)
        assert "".join(t.value for t in tokens) == code

    def test_response_status(self) -> None:
        lexer = get_lexer("http")
        code = "HTTP/1.1 200 OK"
        tokens = list(lexer.tokenize(code))
        assert any(t.type == TokenType.GENERIC_HEADING for t in tokens)
        assert "".join(t.value for t in tokens) == code

    def test_header_line(self) -> None:
        lexer = get_lexer("http")
        code = "Content-Type: application/json"
        tokens = list(lexer.tokenize(code))
        assert any(t.type == TokenType.NAME_ATTRIBUTE for t in tokens)
        assert "".join(t.value for t in tokens) == code


class TestMergeLexer:
    """Edge cases for merge conflict lexer."""

    def test_empty_input(self) -> None:
        lexer = get_lexer("merge")
        tokens = list(lexer.tokenize(""))
        assert tokens == []

    def test_markers_only_reconstructs(self) -> None:
        lexer = get_lexer("merge")
        code = "<<<<<<< HEAD\n=======\n>>>>>>> branch"
        tokens = list(lexer.tokenize(code))
        assert "".join(t.value for t in tokens) == code

    def test_deleted_heading_inserted_types(self) -> None:
        lexer = get_lexer("merge")
        code = "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> branch"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.GENERIC_DELETED in types
        assert TokenType.GENERIC_HEADING in types
        assert TokenType.GENERIC_INSERTED in types
        assert "".join(t.value for t in tokens) == code
