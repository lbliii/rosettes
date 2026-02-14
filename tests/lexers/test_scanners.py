"""Unit tests for shared scanner primitives in _scanners."""

from __future__ import annotations

import pytest

try:
    from rosettes.lexers._scanners import scan_line
except ImportError:
    pytest.skip("scan_line not in installed rosettes (use pip install -e .)", allow_module_level=True)


class TestScanLine:
    """Tests for scan_line()."""

    def test_empty_string(self) -> None:
        content, new_pos, has_newline = scan_line("", 0, 0)
        assert content == ""
        assert new_pos == 0
        assert has_newline is False

    def test_single_line_no_newline(self) -> None:
        content, new_pos, has_newline = scan_line("hello", 0, 5)
        assert content == "hello"
        assert new_pos == 5
        assert has_newline is False

    def test_single_line_with_newline(self) -> None:
        content, new_pos, has_newline = scan_line("hello\n", 0, 6)
        assert content == "hello"
        assert new_pos == 6
        assert has_newline is True

    def test_multiline_first_line(self) -> None:
        content, new_pos, has_newline = scan_line("a\nb\nc", 0, 5)
        assert content == "a"
        assert new_pos == 2
        assert has_newline is True

    def test_multiline_second_line(self) -> None:
        content, new_pos, has_newline = scan_line("a\nb\nc", 2, 5)
        assert content == "b"
        assert new_pos == 4
        assert has_newline is True

    def test_multiline_last_line_no_trailing_newline(self) -> None:
        content, new_pos, has_newline = scan_line("a\nb\nc", 4, 5)
        assert content == "c"
        assert new_pos == 5
        assert has_newline is False

    def test_slice_with_end_parameter(self) -> None:
        content, new_pos, has_newline = scan_line("hello world", 0, 5)
        assert content == "hello"
        assert new_pos == 5
        assert has_newline is False

    def test_empty_line(self) -> None:
        content, new_pos, has_newline = scan_line("\n", 0, 1)
        assert content == ""
        assert new_pos == 1
        assert has_newline is True
