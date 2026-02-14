"""Immutable palette definitions for Rosettes theming.

Provides frozen dataclasses for syntax highlighting palettes.
All palettes are thread-safe by design.

**Design Philosophy:**

Palettes define colors for semantic roles, not individual tokens.
This keeps themes manageable (~20 colors) while supporting 100+ token types.

**Architecture:**

- `SyntaxPalette`: Single theme with fixed colors
  - ~20 color slots for semantic roles
  - Style modifiers (bold, italic)
  - CSS variable generation

- `AdaptivePalette`: Light/dark mode support
  - Contains two SyntaxPalette instances
  - Generates `@media (prefers-color-scheme)` CSS

**Creating Palettes:**

Minimal (only required fields):

```python
>>> palette = SyntaxPalette(
...     name="minimal",
...     background="#1a1a1a",
...     text="#f0f0f0",
... )
>>> filled = palette.with_defaults()  # Fills missing colors
```

Complete (all roles specified):

```python
>>> palette = SyntaxPalette(
...     name="complete",
...     background="#1a1a1a",
...     text="#f0f0f0",
...     string="#98c379",
...     number="#d19a66",
...     function="#61afef",
...     # ... all other roles ...
... )
```

**CSS Generation:**

```python
>>> css_vars = palette.to_css_vars(indent=2)
>>> print(css_vars)
  --syntax-bg: #1a1a1a;
  --syntax-string: #98c379;
  ...
```

**Thread-Safety:**

Both classes are frozen dataclasses. Once created, they cannot be
modified. Safe to share across threads.

**See Also:**

- `rosettes.themes`: Palette registry and built-in palettes
- `rosettes.themes._roles`: SyntaxRole enum (what the colors are for)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from rosettes.themes._contrast import contrast_ratio, passes_aa, passes_aaa
from rosettes.themes._roles import SyntaxRole

if TYPE_CHECKING:
    from typing import Literal

    CssClassStyle = Literal["semantic", "pygments"]

# Role -> palette attribute for contrast validation
_ROLE_TO_PALETTE_ATTR: dict[SyntaxRole, str] = {
    SyntaxRole.CONTROL_FLOW: "control_flow",
    SyntaxRole.DECLARATION: "declaration",
    SyntaxRole.IMPORT: "import_",
    SyntaxRole.STRING: "string",
    SyntaxRole.DOCSTRING: "docstring",
    SyntaxRole.NUMBER: "number",
    SyntaxRole.BOOLEAN: "boolean",
    SyntaxRole.TYPE: "type_",
    SyntaxRole.FUNCTION: "function",
    SyntaxRole.VARIABLE: "variable",
    SyntaxRole.CONSTANT: "constant",
    SyntaxRole.COMMENT: "comment",
    SyntaxRole.ERROR: "error",
    SyntaxRole.WARNING: "warning",
    SyntaxRole.ADDED: "added",
    SyntaxRole.REMOVED: "removed",
    SyntaxRole.TEXT: "text",
    SyntaxRole.MUTED: "muted",
    SyntaxRole.PUNCTUATION: "punctuation",
    SyntaxRole.OPERATOR: "operator",
    SyntaxRole.ATTRIBUTE: "attribute",
    SyntaxRole.NAMESPACE: "namespace",
    SyntaxRole.TAG: "tag",
    SyntaxRole.REGEX: "regex",
    SyntaxRole.ESCAPE: "escape",
}

__all__ = ["AdaptivePalette", "SyntaxPalette"]


@dataclass(frozen=True, slots=True)
class SyntaxPalette:
    """Immutable syntax highlighting palette.

    Thread-safe by design. Defines ~20 semantic color slots
    instead of 100+ individual token colors.

    Required Fields:
        name: Unique identifier for the palette
        background: Background color for code blocks
        text: Default text color

    Optional Fields:
        All other fields default to empty string and are filled
        by with_defaults() using sensible fallbacks.

    Example:
        >>> palette = SyntaxPalette(
        ...     name="my-theme",
        ...     background="#282c34",
        ...     text="#abb2bf",
        ...     string="#98c379",
        ...     function="#61afef",
        ... )
        >>> filled = palette.with_defaults()
        >>> css = filled.to_css_vars()
    """

    # Required fields
    name: str
    background: str
    text: str

    # Background variants
    background_highlight: str = ""

    # Control & Structure
    control_flow: str = ""
    declaration: str = ""
    import_: str = ""

    # Data & Literals
    string: str = ""
    number: str = ""
    boolean: str = ""

    # Identifiers
    type_: str = ""
    function: str = ""
    variable: str = ""
    constant: str = ""

    # Documentation
    comment: str = ""
    docstring: str = ""

    # Feedback
    error: str = ""
    warning: str = ""
    added: str = ""
    removed: str = ""

    # Base
    muted: str = ""

    # Additional roles
    punctuation: str = ""
    operator: str = ""
    attribute: str = ""
    namespace: str = ""
    tag: str = ""
    regex: str = ""
    escape: str = ""

    # Style modifiers
    bold_control: bool = True
    bold_declaration: bool = True
    bold_type: bool = False
    italic_comment: bool = True
    italic_docstring: bool = True
    italic_variable: bool = False

    def __post_init__(self) -> None:
        """Validate palette after initialization."""
        if not self.name:
            raise ValueError("Palette name is required")
        if not self.background:
            raise ValueError("Background color is required")
        if not self.text:
            raise ValueError("Text color is required")

    def with_defaults(self) -> SyntaxPalette:
        """Return a new palette with empty fields filled from defaults."""
        return SyntaxPalette(
            name=self.name,
            background=self.background,
            text=self.text,
            background_highlight=self.background_highlight or self.background,
            control_flow=self.control_flow or self.text,
            declaration=self.declaration or self.text,
            import_=self.import_ or self.control_flow or self.text,
            string=self.string or self.text,
            number=self.number or self.text,
            boolean=self.boolean or self.number or self.text,
            type_=self.type_ or self.text,
            function=self.function or self.text,
            variable=self.variable or self.text,
            constant=self.constant or self.text,
            comment=self.comment or self.muted or self.text,
            docstring=self.docstring or self.comment or self.muted or self.text,
            error=self.error or "#ff0000",
            warning=self.warning or "#ffcc00",
            added=self.added or "#00ff00",
            removed=self.removed or "#ff0000",
            muted=self.muted or self.text,
            punctuation=self.punctuation or self.muted or self.text,
            operator=self.operator or self.control_flow or self.text,
            attribute=self.attribute or self.declaration or self.text,
            namespace=self.namespace or self.type_ or self.text,
            tag=self.tag or self.type_ or self.text,
            regex=self.regex or self.string or self.text,
            escape=self.escape or self.string or self.text,
            bold_control=self.bold_control,
            bold_declaration=self.bold_declaration,
            bold_type=self.bold_type,
            italic_comment=self.italic_comment,
            italic_docstring=self.italic_docstring,
            italic_variable=self.italic_variable,
        )

    def validate_contrast(
        self,
        *,
        level: Literal["AA", "AAA"] = "AA",
        large_text: bool = False,
    ) -> dict[str, str]:
        """Return dict of role -> message for roles failing WCAG contrast.

        Args:
            level: "AA" (4.5:1 normal, 3:1 large) or "AAA" (7:1 normal, 4.5:1 large)
            large_text: If True, use large-text thresholds.

        Returns:
            Empty dict if all roles pass. Otherwise role name -> failure message.

        Example:
            >>> palette = get_palette("bengal-tiger")
            >>> failures = palette.validate_contrast()
            >>> if failures:
            ...     for role, msg in failures.items():
            ...         print(f"{role}: {msg}")
        """
        filled = self.with_defaults()
        passes = passes_aaa if level == "AAA" else passes_aa
        min_ratio = (4.5 if large_text else 7.0) if level == "AAA" else (3.0 if large_text else 4.5)
        failures: dict[str, str] = {}

        for role, attr in _ROLE_TO_PALETTE_ATTR.items():
            color = getattr(filled, attr)
            if not color:
                continue
            try:
                ratio = contrast_ratio(color, filled.background)
                if not passes(ratio, large_text=large_text):
                    failures[role.value] = (
                        f"contrast {ratio:.1f}:1 (need {min_ratio}:1 for {level})"
                    )
            except ValueError:
                failures[role.value] = "invalid hex color"

        return failures

    def to_css_vars(self, indent: int = 0) -> str:
        """Generate CSS custom property declarations."""
        prefix = " " * indent
        filled = self.with_defaults()

        lines = [
            f"{prefix}--syntax-bg: {filled.background};",
            f"{prefix}--syntax-bg-highlight: {filled.background_highlight};",
            f"{prefix}--syntax-control: {filled.control_flow};",
            f"{prefix}--syntax-declaration: {filled.declaration};",
            f"{prefix}--syntax-import: {filled.import_};",
            f"{prefix}--syntax-string: {filled.string};",
            f"{prefix}--syntax-number: {filled.number};",
            f"{prefix}--syntax-boolean: {filled.boolean};",
            f"{prefix}--syntax-type: {filled.type_};",
            f"{prefix}--syntax-function: {filled.function};",
            f"{prefix}--syntax-variable: {filled.variable};",
            f"{prefix}--syntax-constant: {filled.constant};",
            f"{prefix}--syntax-comment: {filled.comment};",
            f"{prefix}--syntax-docstring: {filled.docstring};",
            f"{prefix}--syntax-error: {filled.error};",
            f"{prefix}--syntax-warning: {filled.warning};",
            f"{prefix}--syntax-added: {filled.added};",
            f"{prefix}--syntax-removed: {filled.removed};",
            f"{prefix}--syntax-text: {filled.text};",
            f"{prefix}--syntax-muted: {filled.muted};",
            f"{prefix}--syntax-punctuation: {filled.punctuation};",
            f"{prefix}--syntax-operator: {filled.operator};",
            f"{prefix}--syntax-attribute: {filled.attribute};",
            f"{prefix}--syntax-namespace: {filled.namespace};",
            f"{prefix}--syntax-tag: {filled.tag};",
            f"{prefix}--syntax-regex: {filled.regex};",
            f"{prefix}--syntax-escape: {filled.escape};",
        ]
        return "\n".join(lines)

    def generate_css(self, *, class_style: CssClassStyle = "semantic") -> str:
        """Generate complete CSS stylesheet for syntax highlighting.

        Generates CSS rules for all semantic roles, suitable for use with
        the HTML formatter.

        Args:
            class_style: CSS class naming style:
                - "semantic": Readable classes like .syntax-function
                - "pygments": Pygments-compatible classes like .nf

        Returns:
            Complete CSS stylesheet as a string.

        Example:
            >>> palette = get_palette("bengal-tiger")
            >>> css = palette.generate_css()
            >>> ".syntax-function" in css
            True
        """
        from rosettes.themes._mapping import PYGMENTS_CLASS_MAP

        filled = self.with_defaults()

        # Map roles to their colors and CSS properties
        def _bold(x: bool) -> list[str]:
            return ["font-weight: bold"] if x else []

        def _italic(x: bool) -> list[str]:
            return ["font-style: italic"] if x else []

        role_colors: dict[SyntaxRole, tuple[str, list[str]]] = {
            SyntaxRole.CONTROL_FLOW: (filled.control_flow, _bold(filled.bold_control)),
            SyntaxRole.DECLARATION: (filled.declaration, _bold(filled.bold_declaration)),
            SyntaxRole.IMPORT: (filled.import_, []),
            SyntaxRole.STRING: (filled.string, []),
            SyntaxRole.DOCSTRING: (filled.docstring, _italic(filled.italic_docstring)),
            SyntaxRole.NUMBER: (filled.number, []),
            SyntaxRole.BOOLEAN: (filled.boolean, []),
            SyntaxRole.TYPE: (filled.type_, _bold(filled.bold_type)),
            SyntaxRole.FUNCTION: (filled.function, []),
            SyntaxRole.VARIABLE: (filled.variable, _italic(filled.italic_variable)),
            SyntaxRole.CONSTANT: (filled.constant, []),
            SyntaxRole.COMMENT: (filled.comment, _italic(filled.italic_comment)),
            SyntaxRole.ERROR: (filled.error, []),
            SyntaxRole.WARNING: (filled.warning, []),
            SyntaxRole.ADDED: (filled.added, []),
            SyntaxRole.REMOVED: (filled.removed, []),
            SyntaxRole.TEXT: (filled.text, []),
            SyntaxRole.MUTED: (filled.muted, []),
            SyntaxRole.PUNCTUATION: (filled.punctuation, []),
            SyntaxRole.OPERATOR: (filled.operator, []),
            SyntaxRole.ATTRIBUTE: (filled.attribute, []),
            SyntaxRole.NAMESPACE: (filled.namespace, []),
            SyntaxRole.TAG: (filled.tag, []),
            SyntaxRole.REGEX: (filled.regex, []),
            SyntaxRole.ESCAPE: (filled.escape, []),
        }

        css_parts: list[str] = []

        # Add CSS custom properties block
        css_parts.append(f"/* {self.name} - Generated by Rosettes */")
        css_parts.append(":root {")
        css_parts.append(self.to_css_vars(indent=2))
        css_parts.append("}")
        css_parts.append("")

        # Add base styles
        css_parts.append(".rosettes, .highlight {")
        css_parts.append(f"  background-color: {filled.background};")
        css_parts.append(f"  color: {filled.text};")
        css_parts.append("}")
        css_parts.append("")

        # Add role-based styles
        for role, (color, extra_props) in role_colors.items():
            if class_style == "semantic":
                class_name = f".syntax-{role.value}"
            else:
                # Pygments style
                pygments_class = PYGMENTS_CLASS_MAP.get(role, "")
                if not pygments_class:
                    continue  # Skip roles without Pygments mapping
                class_name = f".{pygments_class}"

            props = [f"color: {color}"]
            props.extend(extra_props)

            css_parts.append(f"{class_name} {{")
            css_parts.extend(f"  {prop};" for prop in props)
            css_parts.append("}")

        return "\n".join(css_parts)


@dataclass(frozen=True, slots=True)
class AdaptivePalette:
    """Theme that adapts to light/dark mode preference.

    Wraps two SyntaxPalette instances for light and dark mode.
    Generates CSS with @media (prefers-color-scheme) queries.

    Thread-safe: frozen dataclass containing frozen palettes.

    Attributes:
        name: Unique identifier for the adaptive palette
        light: Palette for light mode (prefers-color-scheme: light)
        dark: Palette for dark mode (prefers-color-scheme: dark)

    Example:
        >>> from rosettes.themes import GITHUB_LIGHT, GITHUB_DARK
        >>> adaptive = AdaptivePalette(
        ...     name="github-adaptive",
        ...     light=GITHUB_LIGHT,
        ...     dark=GITHUB_DARK,
        ... )

    CSS Generation:
        Adaptive palettes generate CSS with media queries:

        @media (prefers-color-scheme: light) {
          :root { --syntax-bg: #ffffff; ... }
        }
        @media (prefers-color-scheme: dark) {
          :root { --syntax-bg: #0d1117; ... }
        }
    """

    name: str
    light: SyntaxPalette
    dark: SyntaxPalette

    def __post_init__(self) -> None:
        """Validate adaptive palette."""
        if not self.name:
            raise ValueError("Palette name is required")

    def validate_contrast(
        self,
        *,
        level: Literal["AA", "AAA"] = "AA",
        large_text: bool = False,
    ) -> dict[str, str]:
        """Return contrast failures for both light and dark palettes.

        Combines results with "light." and "dark." prefix for adaptive palettes.
        """
        failures: dict[str, str] = {}
        for prefix, palette in [("light.", self.light), ("dark.", self.dark)]:
            for role, msg in palette.validate_contrast(level=level, large_text=large_text).items():
                failures[f"{prefix}{role}"] = msg
        return failures

    def generate_css(self, *, class_style: CssClassStyle = "semantic") -> str:
        """Generate adaptive CSS with light/dark mode support.

        Generates CSS with @media (prefers-color-scheme) queries for
        automatic light/dark mode switching.

        Args:
            class_style: CSS class naming style:
                - "semantic": Readable classes like .syntax-function
                - "pygments": Pygments-compatible classes like .nf

        Returns:
            Complete CSS stylesheet with media queries.

        Example:
            >>> adaptive = get_palette("github")
            >>> css = adaptive.generate_css()
            >>> "@media (prefers-color-scheme: dark)" in css
            True
        """
        css_parts: list[str] = []

        css_parts.append(f"/* {self.name} - Adaptive theme generated by Rosettes */")
        css_parts.append("")

        # Light mode (default)
        css_parts.append("@media (prefers-color-scheme: light) {")
        light_css = self.light.generate_css(class_style=class_style)
        # Indent the light CSS
        css_parts.extend(f"  {line}" for line in light_css.split("\n") if line.strip())
        css_parts.append("}")
        css_parts.append("")

        # Dark mode
        css_parts.append("@media (prefers-color-scheme: dark) {")
        dark_css = self.dark.generate_css(class_style=class_style)
        css_parts.extend(f"  {line}" for line in dark_css.split("\n") if line.strip())
        css_parts.append("}")

        return "\n".join(css_parts)
