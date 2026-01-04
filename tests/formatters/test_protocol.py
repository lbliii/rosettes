"""Tests for Formatter protocol compliance across all formatters."""

from __future__ import annotations

import pytest

from rosettes import Token, TokenType
from rosettes._protocol import Formatter
from rosettes.formatters import HtmlFormatter, NullFormatter, TerminalFormatter

# All built-in formatters should implement the full protocol
FORMATTERS = [
    HtmlFormatter(),
    TerminalFormatter(),
    NullFormatter(),
]


class TestFormatterProtocol:
    """Test all formatters implement Formatter protocol."""

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_implements_protocol(self, formatter: Formatter) -> None:
        """All formatters should implement Formatter protocol."""
        assert isinstance(formatter, Formatter)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_has_name_property(self, formatter: Formatter) -> None:
        """All formatters should have a name property."""
        assert isinstance(formatter.name, str)
        assert len(formatter.name) > 0

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_has_format_method(self, formatter: Formatter) -> None:
        """All formatters should have format() method."""
        assert hasattr(formatter, "format")
        assert callable(formatter.format)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_has_format_fast_method(self, formatter: Formatter) -> None:
        """All formatters should have format_fast() method."""
        assert hasattr(formatter, "format_fast")
        assert callable(formatter.format_fast)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_has_format_string_method(self, formatter: Formatter) -> None:
        """All formatters should have format_string() method."""
        assert hasattr(formatter, "format_string")
        assert callable(formatter.format_string)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_has_format_string_fast_method(self, formatter: Formatter) -> None:
        """All formatters should have format_string_fast() method."""
        assert hasattr(formatter, "format_string_fast")
        assert callable(formatter.format_string_fast)


class TestFormatterBehavior:
    """Test formatters produce consistent output."""

    @pytest.fixture
    def sample_tokens(self) -> list[Token]:
        """Sample tokens for testing."""
        return [
            Token(TokenType.KEYWORD, "def", 1, 1),
            Token(TokenType.WHITESPACE, " ", 1, 4),
            Token(TokenType.NAME, "foo", 1, 5),
            Token(TokenType.PUNCTUATION, "(", 1, 8),
            Token(TokenType.PUNCTUATION, ")", 1, 9),
            Token(TokenType.PUNCTUATION, ":", 1, 10),
            Token(TokenType.WHITESPACE, " ", 1, 11),
            Token(TokenType.KEYWORD, "pass", 1, 12),
        ]

    @pytest.fixture
    def sample_tuples(self) -> list[tuple[TokenType, str]]:
        """Sample token tuples for fast path testing."""
        return [
            (TokenType.KEYWORD, "def"),
            (TokenType.WHITESPACE, " "),
            (TokenType.NAME, "foo"),
            (TokenType.PUNCTUATION, "("),
            (TokenType.PUNCTUATION, ")"),
            (TokenType.PUNCTUATION, ":"),
            (TokenType.WHITESPACE, " "),
            (TokenType.KEYWORD, "pass"),
        ]

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_format_returns_iterator(
        self, formatter: Formatter, sample_tokens: list[Token]
    ) -> None:
        """format() should return an iterator of strings."""
        result = formatter.format(iter(sample_tokens))
        chunks = list(result)

        assert all(isinstance(chunk, str) for chunk in chunks)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_format_fast_returns_iterator(
        self, formatter: Formatter, sample_tuples: list[tuple[TokenType, str]]
    ) -> None:
        """format_fast() should return an iterator of strings."""
        result = formatter.format_fast(iter(sample_tuples))
        chunks = list(result)

        assert all(isinstance(chunk, str) for chunk in chunks)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_format_string_returns_str(
        self, formatter: Formatter, sample_tokens: list[Token]
    ) -> None:
        """format_string() should return a string."""
        result = formatter.format_string(iter(sample_tokens))
        assert isinstance(result, str)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_format_string_fast_returns_str(
        self, formatter: Formatter, sample_tuples: list[tuple[TokenType, str]]
    ) -> None:
        """format_string_fast() should return a string."""
        result = formatter.format_string_fast(iter(sample_tuples))
        assert isinstance(result, str)

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_empty_tokens_handled(self, formatter: Formatter) -> None:
        """All formatters should handle empty token streams."""
        result_format = formatter.format_string(iter([]))
        result_fast = formatter.format_string_fast(iter([]))

        assert isinstance(result_format, str)
        assert isinstance(result_fast, str)


class TestFormatterThreadSafety:
    """Test formatters are thread-safe (immutable)."""

    @pytest.mark.parametrize("formatter", FORMATTERS, ids=lambda f: f.name)
    def test_formatter_is_frozen(self, formatter: Formatter) -> None:
        """All formatters should be immutable (frozen dataclass)."""
        # Try to modify the formatter — should raise
        with pytest.raises((AttributeError, TypeError)):
            formatter.name = "modified"  # type: ignore[misc]
