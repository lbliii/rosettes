"""Tests for NullFormatter."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from rosettes import Token, TokenType, highlight
from rosettes._protocol import Formatter
from rosettes.formatters import NullFormatter


class TestNullFormatterBasics:
    """Test NullFormatter basic functionality."""

    def test_name_property(self) -> None:
        """NullFormatter should have 'null' name."""
        formatter = NullFormatter()
        assert formatter.name == "null"

    def test_format_yields_raw_values(self) -> None:
        """format() should yield raw token values."""
        tokens = [
            Token(TokenType.KEYWORD, "def", 1, 1),
            Token(TokenType.WHITESPACE, " ", 1, 4),
            Token(TokenType.NAME, "foo", 1, 5),
        ]
        formatter = NullFormatter()

        result = list(formatter.format(iter(tokens)))

        assert result == ["def", " ", "foo"]

    def test_format_fast_yields_raw_values(self) -> None:
        """format_fast() should yield raw token values from tuples."""
        tokens = [
            (TokenType.KEYWORD, "def"),
            (TokenType.WHITESPACE, " "),
            (TokenType.NAME, "foo"),
        ]
        formatter = NullFormatter()

        result = list(formatter.format_fast(iter(tokens)))

        assert result == ["def", " ", "foo"]

    def test_format_string(self) -> None:
        """format_string() should return concatenated values."""
        tokens = [
            Token(TokenType.KEYWORD, "def", 1, 1),
            Token(TokenType.WHITESPACE, " ", 1, 4),
            Token(TokenType.NAME, "foo", 1, 5),
        ]
        formatter = NullFormatter()

        result = formatter.format_string(iter(tokens))

        assert result == "def foo"

    def test_format_string_fast(self) -> None:
        """format_string_fast() should return concatenated values."""
        tokens = [
            (TokenType.KEYWORD, "def"),
            (TokenType.WHITESPACE, " "),
            (TokenType.NAME, "foo"),
        ]
        formatter = NullFormatter()

        result = formatter.format_string_fast(iter(tokens))

        assert result == "def foo"


class TestNullFormatterWithHighlight:
    """Test NullFormatter with highlight() function."""

    def test_highlight_with_null_formatter(self) -> None:
        """highlight() with formatter='null' should return raw text."""
        code = "def foo(): pass"
        result = highlight(code, "python", formatter="null")

        assert result == code

    def test_highlight_with_formatter_instance(self) -> None:
        """highlight() should accept NullFormatter instance."""
        code = "x = 1"
        formatter = NullFormatter()
        result = highlight(code, "python", formatter=formatter)

        assert result == code


class TestNullFormatterProtocol:
    """Test NullFormatter implements Formatter protocol."""

    def test_implements_formatter_protocol(self) -> None:
        """NullFormatter should satisfy Formatter protocol."""
        formatter = NullFormatter()
        assert isinstance(formatter, Formatter)

    def test_is_frozen_dataclass(self) -> None:
        """NullFormatter should be a frozen dataclass for thread-safety."""
        formatter = NullFormatter()

        # Frozen dataclass raises on attribute assignment
        with pytest.raises((FrozenInstanceError, TypeError, AttributeError)):
            formatter.name = "modified"  # type: ignore[misc]

    def test_has_slots(self) -> None:
        """NullFormatter should use slots for memory efficiency."""
        formatter = NullFormatter()
        assert hasattr(formatter, "__slots__") or not hasattr(formatter, "__dict__")


class TestNullFormatterEdgeCases:
    """Test edge cases."""

    def test_empty_tokens(self) -> None:
        """Empty token stream should produce empty string."""
        formatter = NullFormatter()
        assert formatter.format_string(iter([])) == ""
        assert formatter.format_string_fast(iter([])) == ""

    def test_multiline_code(self) -> None:
        """Multiline code should be preserved."""
        code = "def foo():\n    pass"
        result = highlight(code, "python", formatter="null")
        assert result == code

    def test_unicode(self) -> None:
        """Unicode should be preserved."""
        code = 'x = "héllo wörld 日本語"'
        result = highlight(code, "python", formatter="null")
        assert result == code

