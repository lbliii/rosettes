"""Comprehensive tests for C# lexer.

Tests token accuracy for C# constructs:
- Keywords (class, var, async, await, etc.)
- Types (int, string, etc.)
- @ prefix (attributes, verbatim identifiers)
- Strings: regular, interpolated, verbatim, raw triple-quote
- Comments: //, /* */, ///
- Operators: =>, ??, ?., etc.
"""

from __future__ import annotations

import pytest

from rosettes import TokenType


class TestCSharpKeywords:
    """Test C# keyword tokenization."""

    def test_class_keyword(self, csharp_lexer) -> None:
        """'class' should be KEYWORD_DECLARATION."""
        tokens = list(csharp_lexer.tokenize("class"))
        assert tokens[0].type == TokenType.KEYWORD_DECLARATION
        assert tokens[0].value == "class"

    def test_var_keyword(self, csharp_lexer) -> None:
        """'var' should be KEYWORD."""
        tokens = list(csharp_lexer.tokenize("var"))
        assert tokens[0].type == TokenType.KEYWORD

    def test_namespace_keyword(self, csharp_lexer) -> None:
        """'namespace' should be KEYWORD_NAMESPACE."""
        tokens = list(csharp_lexer.tokenize("namespace"))
        assert tokens[0].type == TokenType.KEYWORD_NAMESPACE

    def test_using_keyword(self, csharp_lexer) -> None:
        """'using' should be KEYWORD_NAMESPACE."""
        tokens = list(csharp_lexer.tokenize("using"))
        assert tokens[0].type == TokenType.KEYWORD_NAMESPACE

    def test_async_await_keywords(self, csharp_lexer) -> None:
        """'async' and 'await' should be KEYWORD."""
        code = "async await"
        tokens = list(csharp_lexer.tokenize(code))
        values = [t.value for t in tokens if t.type == TokenType.KEYWORD]
        assert "async" in values
        assert "await" in values


class TestCSharpTypes:
    """Test C# type tokenization."""

    def test_int_type(self, csharp_lexer) -> None:
        """'int' should be KEYWORD_TYPE."""
        tokens = list(csharp_lexer.tokenize("int"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE

    def test_string_type(self, csharp_lexer) -> None:
        """'string' should be KEYWORD_TYPE."""
        tokens = list(csharp_lexer.tokenize("string"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE


class TestCSharpAtPrefix:
    """Test C# @ prefix (attributes and verbatim identifiers)."""

    def test_attribute_decorator(self, csharp_lexer) -> None:
        """@Obsolete should be NAME_DECORATOR."""
        code = "@Obsolete"
        tokens = list(csharp_lexer.tokenize(code))
        assert len(tokens) >= 1
        assert tokens[0].type == TokenType.NAME_DECORATOR
        assert tokens[0].value == "@Obsolete"

    def test_verbatim_identifier(self, csharp_lexer) -> None:
        """@class (verbatim) should be NAME (keyword as identifier)."""
        code = "@class"
        tokens = list(csharp_lexer.tokenize(code))
        assert len(tokens) >= 1
        assert tokens[0].type == TokenType.NAME
        assert tokens[0].value == "@class"


class TestCSharpStrings:
    """Test C# string tokenization."""

    def test_regular_string(self, csharp_lexer) -> None:
        """Regular strings should be STRING."""
        code = '"hello"'
        tokens = list(csharp_lexer.tokenize(code))
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1

    def test_interpolated_string(self, csharp_lexer) -> None:
        """$\"...\" interpolated strings should be STRING."""
        code = r'$"hello {name}"'
        tokens = list(csharp_lexer.tokenize(code))
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1

    def test_verbatim_string(self, csharp_lexer) -> None:
        """@\"...\" verbatim strings should be STRING."""
        code = '@"verbatim\npath"'
        tokens = list(csharp_lexer.tokenize(code))
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1


class TestCSharpComments:
    """Test C# comment tokenization."""

    def test_line_comment(self, csharp_lexer) -> None:
        """// comments should be COMMENT_SINGLE."""
        code = "// comment"
        tokens = list(csharp_lexer.tokenize(code))
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT_SINGLE]
        assert len(comment_tokens) == 1

    def test_block_comment(self, csharp_lexer) -> None:
        """/* */ comments should be COMMENT_MULTILINE."""
        code = "/* block */"
        tokens = list(csharp_lexer.tokenize(code))
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT_MULTILINE]
        assert len(comment_tokens) == 1

    def test_doc_comment(self, csharp_lexer) -> None:
        """/** */ doc comments should be STRING_DOC."""
        code = "/** doc */"
        tokens = list(csharp_lexer.tokenize(code))
        doc_tokens = [t for t in tokens if t.type == TokenType.STRING_DOC]
        assert len(doc_tokens) == 1


class TestCSharpOperators:
    """Test C# operator tokenization."""

    def test_lambda_arrow(self, csharp_lexer) -> None:
        """=> should be OPERATOR."""
        code = "x => x"
        tokens = list(csharp_lexer.tokenize(code))
        arrow_tokens = [t for t in tokens if t.value == "=>"]
        assert len(arrow_tokens) == 1
        assert arrow_tokens[0].type == TokenType.OPERATOR

    def test_null_coalescing(self, csharp_lexer) -> None:
        """?? should be OPERATOR."""
        code = "x ?? y"
        tokens = list(csharp_lexer.tokenize(code))
        null_coalesce = [t for t in tokens if t.value == "??"]
        assert len(null_coalesce) == 1
        assert null_coalesce[0].type == TokenType.OPERATOR


class TestCSharpComplex:
    """Test complex C# code."""

    def test_class_with_method(self, csharp_lexer) -> None:
        """Class with method should tokenize correctly."""
        code = "class Foo { public void M() { } }"
        tokens = list(csharp_lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.KEYWORD_DECLARATION in types
        assert TokenType.NAME_CLASS in types
        assert TokenType.KEYWORD in types

    def test_fixture_basics(self, csharp_lexer) -> None:
        """Fixture basics.cs should tokenize without error."""
        from pathlib import Path

        fixture_path = Path(__file__).parent.parent / "fixtures" / "csharp" / "basics.cs"
        if not fixture_path.exists():
            pytest.skip("fixtures/csharp/basics.cs not found")
        code = fixture_path.read_text(encoding="utf-8")
        tokens = list(csharp_lexer.tokenize(code))
        assert len(tokens) > 0
        error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
        assert len(error_tokens) == 0
