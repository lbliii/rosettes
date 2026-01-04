"""Tests for CSS generation from palettes."""

from __future__ import annotations

import pytest

from rosettes.themes import get_palette, list_palettes


class TestPaletteApi:
    """Verify palette API exists before testing CSS generation."""

    def test_list_palettes_returns_list(self) -> None:
        """list_palettes should return a list."""
        palettes = list_palettes()
        assert isinstance(palettes, list)
        assert len(palettes) >= 1, "No palettes registered"

    def test_bengal_tiger_palette_exists(self) -> None:
        """Default palette should exist."""
        palettes = list_palettes()
        assert "bengal-tiger" in palettes, f"bengal-tiger not in {palettes}"

    def test_get_palette_returns_valid_object(self) -> None:
        """get_palette should return object with required methods."""
        palette = get_palette("bengal-tiger")
        assert palette is not None
        assert hasattr(palette, "name"), "Palette missing 'name' attribute"
        assert hasattr(palette, "generate_css"), "Palette missing 'generate_css' method"
        assert callable(palette.generate_css), "generate_css must be callable"

    def test_get_palette_invalid_name_raises(self) -> None:
        """get_palette should raise for unknown palette."""
        with pytest.raises(LookupError):
            get_palette("nonexistent-palette-name")


class TestCssGeneration:
    """Test CSS generation from palettes."""

    @pytest.mark.parametrize("palette_name", list_palettes())
    def test_css_generation(self, palette_name: str) -> None:
        """CSS should be generated for all palettes."""
        palette = get_palette(palette_name)
        css = palette.generate_css()

        assert isinstance(css, str), f"Expected str, got {type(css)}"
        assert len(css) > 0, "Generated CSS is empty"
        # Should have CSS rules
        assert "{" in css and "}" in css, "Missing CSS rule blocks"
        # Should have color values
        assert "#" in css or "rgb" in css, "No color values in CSS"

    @pytest.mark.parametrize("palette_name", list_palettes())
    def test_css_contains_core_token_types(self, palette_name: str) -> None:
        """CSS should contain styles for core token types."""
        palette = get_palette(palette_name)
        css = palette.generate_css()

        # Check for common token class patterns (semantic or pygments style)
        has_syntax_classes = ".syntax-" in css or ".s" in css or ".k" in css
        assert has_syntax_classes, f"CSS missing core token styles: {css[:200]}..."

    def test_css_valid_syntax(self) -> None:
        """Generated CSS should have valid syntax."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css()

        # Basic syntax checks
        open_braces = css.count("{")
        close_braces = css.count("}")
        assert open_braces == close_braces, (
            f"Mismatched braces: {open_braces} open, {close_braces} close"
        )

        # Should not have obvious errors
        assert "undefined" not in css.lower(), "CSS contains 'undefined'"
        assert "null" not in css.lower(), "CSS contains 'null'"

    def test_css_generation_is_deterministic(self) -> None:
        """Same palette should generate identical CSS."""
        palette = get_palette("bengal-tiger")
        css1 = palette.generate_css()
        css2 = palette.generate_css()
        assert css1 == css2, "CSS generation is non-deterministic"

    def test_css_contains_string_styles(self) -> None:
        """CSS should contain string styles."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css()

        # Should have string-related CSS
        assert ".syntax-string" in css or ".s" in css or "string" in css.lower()

    def test_css_contains_keyword_styles(self) -> None:
        """CSS should contain keyword styles."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css()

        # Should have keyword-related CSS (control in semantic style)
        assert ".syntax-control" in css or ".k" in css or "control" in css.lower()

    def test_semantic_class_style(self) -> None:
        """Semantic style should use readable class names."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css(class_style="semantic")

        assert ".syntax-function" in css
        assert ".syntax-string" in css
        assert ".syntax-comment" in css

    def test_pygments_class_style(self) -> None:
        """Pygments style should use short class names."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css(class_style="pygments")

        assert ".nf" in css  # function
        assert ".s" in css  # string
        assert ".c" in css  # comment


class TestCssVars:
    """Test CSS custom property generation."""

    def test_to_css_vars_returns_string(self) -> None:
        """to_css_vars should return a string."""
        palette = get_palette("bengal-tiger")
        css_vars = palette.to_css_vars()
        assert isinstance(css_vars, str)
        assert len(css_vars) > 0

    def test_css_vars_contain_expected_properties(self) -> None:
        """CSS vars should contain expected custom properties."""
        palette = get_palette("bengal-tiger")
        css_vars = palette.to_css_vars()

        assert "--syntax-bg:" in css_vars
        assert "--syntax-string:" in css_vars
        assert "--syntax-function:" in css_vars
        assert "--syntax-comment:" in css_vars

    def test_css_vars_with_indent(self) -> None:
        """CSS vars should respect indent parameter."""
        palette = get_palette("bengal-tiger")
        css_vars = palette.to_css_vars(indent=4)

        # All lines should start with 4 spaces
        for line in css_vars.split("\n"):
            assert line.startswith("    "), f"Line not indented: {line!r}"


class TestAdaptivePalette:
    """Test adaptive palette CSS generation."""

    def test_github_is_adaptive(self) -> None:
        """GitHub palette should be adaptive."""
        palette = get_palette("github")
        # AdaptivePalette has light and dark attributes
        assert hasattr(palette, "light")
        assert hasattr(palette, "dark")

    def test_adaptive_generates_media_queries(self) -> None:
        """Adaptive palette should generate media queries."""
        palette = get_palette("github")
        css = palette.generate_css()

        assert "@media (prefers-color-scheme: light)" in css
        assert "@media (prefers-color-scheme: dark)" in css
