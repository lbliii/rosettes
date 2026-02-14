"""Tests for WCAG contrast calculation and palette validation."""

from __future__ import annotations

import pytest

from rosettes.themes import get_palette
from rosettes.themes._contrast import contrast_ratio, passes_aa, passes_aaa
from rosettes.themes._palette import SyntaxPalette


class TestContrastRatio:
    """Test contrast ratio calculation."""

    def test_black_white_max_contrast(self) -> None:
        """Black on white should give ~21:1."""
        ratio = contrast_ratio("#000000", "#ffffff")
        assert 20.0 <= ratio <= 22.0

    def test_white_black_same_as_black_white(self) -> None:
        """Contrast ratio is symmetric."""
        assert contrast_ratio("#ffffff", "#000000") == contrast_ratio("#000000", "#ffffff")

    def test_same_color_min_contrast(self) -> None:
        """Same color should give 1:1."""
        assert contrast_ratio("#808080", "#808080") == 1.0

    def test_invalid_hex_raises(self) -> None:
        """Invalid hex should raise ValueError."""
        with pytest.raises(ValueError):
            contrast_ratio("#xyz", "#000000")
        with pytest.raises(ValueError):
            contrast_ratio("#ff", "#000000")


class TestPassesAA:
    """Test WCAG AA threshold checks."""

    def test_45_passes_aa_normal(self) -> None:
        """4.5:1 passes AA for normal text."""
        assert passes_aa(4.5) is True
        assert passes_aa(4.4) is False

    def test_3_passes_aa_large(self) -> None:
        """3:1 passes AA for large text."""
        assert passes_aa(3.0, large_text=True) is True
        assert passes_aa(2.9, large_text=True) is False


class TestPassesAAA:
    """Test WCAG AAA threshold checks."""

    def test_7_passes_aaa_normal(self) -> None:
        """7:1 passes AAA for normal text."""
        assert passes_aaa(7.0) is True
        assert passes_aaa(6.9) is False

    def test_45_passes_aaa_large(self) -> None:
        """4.5:1 passes AAA for large text."""
        assert passes_aaa(4.5, large_text=True) is True
        assert passes_aaa(4.4, large_text=True) is False


class TestValidateContrast:
    """Test palette validate_contrast method."""

    def test_high_contrast_palette_passes_aa(self) -> None:
        """Palette with sufficient contrast should pass AA."""
        # White-on-black gives 21:1; with_defaults cascades to all roles
        palette = SyntaxPalette(
            name="high-contrast",
            background="#000000",
            text="#ffffff",
        )
        failures = palette.validate_contrast(level="AA")
        assert failures == {}

    def test_low_contrast_palette_fails(self) -> None:
        """Palette with low-contrast colors should report failures."""
        palette = SyntaxPalette(
            name="low-contrast",
            background="#1a1a1a",
            text="#2a2a2a",  # Very low contrast
            string="#252525",
        )
        failures = palette.validate_contrast(level="AA")
        assert "text" in failures
        assert "string" in failures

    def test_adaptive_palette_combines_results(self) -> None:
        """AdaptivePalette prefixes light/dark to role names."""
        palette = get_palette("github")
        failures = palette.validate_contrast(level="AA")
        # GitHub palettes are designed for contrast; may pass or fail
        # Just verify the structure if there are failures
        for key in failures:
            assert key.startswith(("light.", "dark."))
