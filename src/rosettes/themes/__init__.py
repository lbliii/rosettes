"""Rosettes themes package.

Semantic token system for syntax highlighting with modern CSS support.
Provides palettes, CSS generation, and accessibility validation.

Design Philosophy:
    Rosettes uses a **semantic role system** instead of individual token colors:

    1. **Roles over Tokens**: ~20 semantic roles (FUNCTION, STRING, COMMENT)
       instead of 100+ token types. Themes define colors for roles.

    2. **Separation of Concerns**: Token → Role mapping is language-agnostic.
       Palettes define colors for roles, not specific syntax.

    3. **CSS Custom Properties**: Palettes generate CSS variables for runtime
       theming without regenerating HTML.

Quick Start:
    >>> from rosettes.themes import MONOKAI, get_palette
    >>> palette = get_palette("monokai")
    >>> css_vars = palette.to_css_vars()

Architecture:
    SyntaxRole: Semantic meaning of code elements (FUNCTION, STRING, etc.)
    TokenType → Role: Mapping from fine-grained tokens to semantic roles
    SyntaxPalette: Immutable color definitions for each role
    AdaptivePalette: Light/dark mode support with CSS media queries

Types:
    - SyntaxRole: Enum of semantic roles
    - SyntaxPalette: Immutable theme definition (~20 color slots)
    - AdaptivePalette: Light/dark adaptive theme

Built-in Palettes:
    Bengal Themes:
        BENGAL_TIGER: Warm orange tones (default)
        BENGAL_SNOW_LYNX: Cool light theme
        BENGAL_CHARCOAL: Dark gray theme
        BENGAL_BLUE: Cool blue tones

    Third-Party Compatible:
        MONOKAI: Classic dark theme
        DRACULA: Purple-accented dark theme
        GITHUB: Light/dark GitHub-style themes

Custom Palettes:
    >>> from rosettes.themes import SyntaxPalette, register_palette
    >>> my_theme = SyntaxPalette(
    ...     name="my-theme",
    ...     background="#1a1a1a",
    ...     text="#f0f0f0",
    ...     string="#98c379",
    ...     function="#61afef",
    ... )
    >>> register_palette(my_theme)

See Also:
    rosettes.themes._roles: SyntaxRole enum definition
    rosettes.themes._mapping: TokenType → SyntaxRole mapping
    rosettes.themes._palette: SyntaxPalette and AdaptivePalette classes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rosettes.themes._mapping import (
    PYGMENTS_CLASS_MAP,
    ROLE_MAPPING,
    get_role,
)
from rosettes.themes._palette import AdaptivePalette, SyntaxPalette
from rosettes.themes._roles import SyntaxRole

# Built-in palettes
from rosettes.themes.palettes import (
    BENGAL_BLUE,
    BENGAL_CHARCOAL,
    BENGAL_SNOW_LYNX,
    BENGAL_TIGER,
    DRACULA,
    GITHUB,
    GITHUB_DARK,
    GITHUB_LIGHT,
    MONOKAI,
)

if TYPE_CHECKING:
    from typing import Literal

    CssClassStyle = Literal["semantic", "pygments"]

__all__ = [
    # Core types
    "SyntaxRole",
    "SyntaxPalette",
    "AdaptivePalette",
    # Mappings
    "ROLE_MAPPING",
    "PYGMENTS_CLASS_MAP",
    "get_role",
    # Bengal palettes
    "BENGAL_TIGER",
    "BENGAL_SNOW_LYNX",
    "BENGAL_CHARCOAL",
    "BENGAL_BLUE",
    # Third-party palettes
    "MONOKAI",
    "DRACULA",
    "GITHUB",
    "GITHUB_LIGHT",
    "GITHUB_DARK",
    # Registry
    "register_palette",
    "get_palette",
    "list_palettes",
    # Type alias
    "Palette",
]


# Type alias for any palette type
Palette = SyntaxPalette | AdaptivePalette


# Palette registry (populated with built-ins)
_PALETTES: dict[str, Palette] = {}


def _init_registry() -> None:
    """Initialize the palette registry with built-in palettes."""
    global _PALETTES

    # Bengal themes
    _PALETTES["bengal-tiger"] = BENGAL_TIGER
    _PALETTES["bengal-snow-lynx"] = BENGAL_SNOW_LYNX
    _PALETTES["bengal-charcoal"] = BENGAL_CHARCOAL
    _PALETTES["bengal-blue"] = BENGAL_BLUE

    # Third-party themes
    _PALETTES["monokai"] = MONOKAI
    _PALETTES["dracula"] = DRACULA
    _PALETTES["github"] = GITHUB
    _PALETTES["github-light"] = GITHUB_LIGHT
    _PALETTES["github-dark"] = GITHUB_DARK


def register_palette(palette: Palette) -> None:
    """Register a custom palette.

    Args:
        palette: The palette to register.
    """
    _PALETTES[palette.name] = palette


def get_palette(name: str) -> Palette:
    """Get a registered palette by name.

    Args:
        name: The palette name.

    Returns:
        The requested palette.

    Raises:
        LookupError: If the palette is not registered.
    """
    # Lazy init
    if not _PALETTES:
        _init_registry()

    if name not in _PALETTES:
        available = ", ".join(sorted(_PALETTES.keys()))
        raise LookupError(f"Unknown syntax theme: {name!r}. Available: {available}")

    return _PALETTES[name]


def list_palettes() -> list[str]:
    """List all registered palette names.

    Returns:
        Sorted list of palette names.
    """
    # Lazy init
    if not _PALETTES:
        _init_registry()

    return sorted(_PALETTES.keys())
