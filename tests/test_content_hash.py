"""Tests for rosettes.content_hash()."""

from __future__ import annotations

from rosettes import content_hash


class TestContentHash:
    """Test content_hash determinism and collision resistance."""

    def test_returns_64_char_hex(self) -> None:
        """content_hash() should return 64-character hex digest."""
        h = content_hash("def foo(): pass", "python")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_deterministic_same_input(self) -> None:
        """Same (code, language) should always yield same hash."""
        code, lang = "def foo(): pass", "python"
        assert content_hash(code, lang) == content_hash(code, lang)

    def test_different_code_different_hash(self) -> None:
        """Different code should yield different hash."""
        h1 = content_hash("x = 1", "python")
        h2 = content_hash("x = 2", "python")
        assert h1 != h2

    def test_different_language_different_hash(self) -> None:
        """Same code, different language should yield different hash."""
        code = "x = 1"
        h1 = content_hash(code, "python")
        h2 = content_hash(code, "javascript")
        assert h1 != h2

    def test_whitespace_changes_hash(self) -> None:
        """Whitespace changes should produce different hash (no normalization)."""
        h1 = content_hash("x=1", "python")
        h2 = content_hash("x = 1", "python")
        assert h1 != h2

    def test_backward_compatible(self) -> None:
        """content_hash(code, lang) without optional args should match original behavior."""
        h = content_hash("x", "py")
        assert len(h) == 64
        assert content_hash("x", "py") == h

    def test_hl_lines_affects_hash(self) -> None:
        """Same code+lang, different hl_lines should yield different hash."""
        code, lang = "x = 1", "python"
        h_base = content_hash(code, lang)
        h_hl1 = content_hash(code, lang, hl_lines=frozenset({1}))
        h_hl2 = content_hash(code, lang, hl_lines=frozenset({2}))
        assert h_base != h_hl1
        assert h_base != h_hl2
        assert h_hl1 != h_hl2

    def test_show_linenos_affects_hash(self) -> None:
        """show_linenos=True should yield different hash than False."""
        code, lang = "x = 1", "python"
        h_base = content_hash(code, lang)
        h_linenos = content_hash(code, lang, show_linenos=True)
        assert h_base != h_linenos

    def test_hl_lines_deterministic(self) -> None:
        """frozenset({1,3}) and frozenset({3,1}) should yield same hash."""
        code, lang = "x = 1", "python"
        h1 = content_hash(code, lang, hl_lines=frozenset({1, 3}))
        h2 = content_hash(code, lang, hl_lines=frozenset({3, 1}))
        assert h1 == h2
