import pytest

from rosettes import get_formatter, list_formatters, supports_formatter
from rosettes.formatters import HtmlFormatter, NullFormatter, TerminalFormatter


def test_get_formatter():
    assert isinstance(get_formatter("html"), HtmlFormatter)
    assert isinstance(get_formatter("terminal"), TerminalFormatter)
    assert isinstance(get_formatter("null"), NullFormatter)

    # Test aliases
    assert isinstance(get_formatter("ansi"), TerminalFormatter)
    assert isinstance(get_formatter("htm"), HtmlFormatter)
    assert isinstance(get_formatter("none"), NullFormatter)


def test_get_formatter_error():
    with pytest.raises(LookupError, match="Unknown formatter"):
        get_formatter("nonexistent")


def test_list_formatters():
    formatters = list_formatters()
    assert "html" in formatters
    assert "terminal" in formatters
    assert "null" in formatters
    assert len(formatters) >= 3


def test_supports_formatter():
    assert supports_formatter("html")
    assert supports_formatter("terminal")
    assert supports_formatter("ansi")
    assert not supports_formatter("nonexistent")


def test_caching():
    # Verify that get_formatter returns the same instance (cached)
    f1 = get_formatter("html")
    f2 = get_formatter("html")
    assert f1 is f2

    f3 = get_formatter("terminal")
    assert f1 is not f3
