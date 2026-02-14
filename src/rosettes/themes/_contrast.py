"""WCAG 2.0 contrast ratio calculation for palette validation.

Pure Python implementation, no external dependencies.
Used by SyntaxPalette.validate_contrast() for accessibility checking.

**WCAG 2.0 Requirements:**
- AA: 4.5:1 for normal text, 3:1 for large text
- AAA: 7:1 for normal text, 4.5:1 for large text

**See Also:**
- https://www.w3.org/TR/WCAG20/#contrast-ratiodef
- rosettes.themes._palette: SyntaxPalette.validate_contrast()
"""

from __future__ import annotations

__all__ = ["contrast_ratio", "passes_aa", "passes_aaa"]


def _hex_to_rgb(hex_str: str) -> tuple[float, float, float]:
    """Parse #RRGGBB to RGB tuple (0-1 range)."""
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: {hex_str!r}")
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return (r, g, b)


def _relative_luminance(rgb: tuple[float, float, float]) -> float:
    """Compute WCAG 2.0 relative luminance for sRGB colors."""
    r, g, b = rgb

    def linearize(c: float) -> float:
        if c <= 0.03928:
            return c / 12.92
        return ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Compute WCAG 2.0 contrast ratio between foreground and background.

    Args:
        fg: Foreground hex color (e.g. "#ffffff")
        bg: Background hex color (e.g. "#000000")

    Returns:
        Contrast ratio (1.0 to 21.0). Higher is better.

    Raises:
        ValueError: If hex colors are invalid.
    """
    l1 = _relative_luminance(_hex_to_rgb(fg))
    l2 = _relative_luminance(_hex_to_rgb(bg))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def passes_aa(ratio: float, *, large_text: bool = False) -> bool:
    """Check if contrast ratio passes WCAG AA.

    Args:
        ratio: Contrast ratio from contrast_ratio()
        large_text: If True, use 3:1 threshold; else 4.5:1.

    Returns:
        True if ratio meets AA requirements.
    """
    return ratio >= (3.0 if large_text else 4.5)


def passes_aaa(ratio: float, *, large_text: bool = False) -> bool:
    """Check if contrast ratio passes WCAG AAA.

    Args:
        ratio: Contrast ratio from contrast_ratio()
        large_text: If True, use 4.5:1 threshold; else 7:1.

    Returns:
        True if ratio meets AAA requirements.
    """
    return ratio >= (4.5 if large_text else 7.0)
