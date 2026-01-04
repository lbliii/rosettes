---
title: Custom Palettes
description: Define and register custom color palettes programmatically
draft: false
weight: 30
lang: en
type: doc
tags:
- themes
- palettes
- customization
keywords:
- custom palette
- syntax palette
- colors
- theming
icon: palette
---

# Custom Palettes

Define color palettes in Python and register them for use across your application.

## Overview

Rosettes uses **semantic roles** instead of individual token colors. This means you define ~20 colors for roles like "control flow" or "string" rather than 100+ token-specific colors.

```python
from rosettes.themes import SyntaxPalette, register_palette

my_palette = SyntaxPalette(
    name="my-theme",
    background="#1a1a2e",
    text="#eaeaea",
    control_flow="#e94560",
    string="#0f3460",
    # ... more colors
)

register_palette(my_palette)
```

---

## SyntaxPalette

The `SyntaxPalette` dataclass defines a complete color scheme:

```python
from rosettes.themes import SyntaxPalette

palette = SyntaxPalette(
    # Required fields
    name="ocean-dark",
    background="#0a192f",
    text="#8892b0",
    
    # Control & Structure
    control_flow="#ff79c6",      # if, for, while, return
    declaration="#bd93f9",       # def, class, let, const
    import_="#ff79c6",           # import, from, use
    
    # Data & Literals
    string="#50fa7b",            # "hello", 'world'
    number="#f1fa8c",            # 42, 3.14
    boolean="#bd93f9",           # True, False
    
    # Identifiers
    type_="#8be9fd",             # int, str, MyClass
    function="#50fa7b",          # function names
    variable="#f8f8f2",          # variable names
    constant="#bd93f9",          # CONSTANTS
    
    # Documentation
    comment="#6272a4",           # # comments
    docstring="#6272a4",         # """docstrings"""
    
    # Feedback (diffs, errors)
    error="#ff5555",
    warning="#ffb86c",
    added="#50fa7b",
    removed="#ff5555",
    
    # Additional
    muted="#6272a4",             # less important elements
    punctuation="#f8f8f2",       # brackets, commas
    operator="#ff79c6",          # +, -, *, /
    attribute="#50fa7b",         # @decorator, .attribute
    namespace="#f8f8f2",         # module.submodule
    tag="#ff79c6",               # HTML/XML tags
    regex="#f1fa8c",             # regular expressions
    escape="#bd93f9",            # escape sequences
    
    # Style modifiers
    bold_control=True,           # bold keywords
    bold_declaration=True,       # bold def/class
    italic_comment=True,         # italic comments
    italic_docstring=True,       # italic docstrings
)
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique palette identifier (used in registry) |
| `background` | Code block background color |
| `text` | Default text color |

### Semantic Roles

| Role | Description | Example Tokens |
|------|-------------|----------------|
| `control_flow` | Control statements | `if`, `for`, `while`, `return` |
| `declaration` | Declarations | `def`, `class`, `let`, `const` |
| `import_` | Import statements | `import`, `from`, `use` |
| `string` | String literals | `"hello"`, `'world'` |
| `number` | Numeric literals | `42`, `3.14`, `0xFF` |
| `boolean` | Boolean values | `True`, `False` |
| `type_` | Type names | `int`, `str`, `MyClass` |
| `function` | Function names | `foo`, `bar` |
| `variable` | Variable names | `x`, `count` |
| `constant` | Constants | `PI`, `MAX_SIZE` |
| `comment` | Comments | `# comment` |
| `docstring` | Documentation | `"""docstring"""` |

---

## AdaptivePalette

For light/dark mode support, use `AdaptivePalette`:

```python
from rosettes.themes import SyntaxPalette, AdaptivePalette, register_palette

light = SyntaxPalette(
    name="ocean-light",
    background="#ffffff",
    text="#1a1a2e",
    control_flow="#d63384",
    string="#198754",
    # ... light theme colors
)

dark = SyntaxPalette(
    name="ocean-dark",
    background="#0a192f",
    text="#8892b0",
    control_flow="#ff79c6",
    string="#50fa7b",
    # ... dark theme colors
)

ocean = AdaptivePalette(
    name="ocean",
    light=light,
    dark=dark,
)

register_palette(ocean)
```

---

## Palette Registry

### Register a Palette

```python
from rosettes.themes import register_palette

register_palette(my_palette)
```

### List Available Palettes

```python
from rosettes.themes import list_palettes

print(list_palettes())
# ['bengal-tiger', 'bengal-snow-lynx', 'dracula', 'monokai', ...]
```

### Get a Palette

```python
from rosettes.themes import get_palette

palette = get_palette("monokai")
print(palette.background)  # #272822
```

---

## Generate CSS

Palettes can generate CSS custom properties:

```python
from rosettes.themes import get_palette

palette = get_palette("dracula")
css_vars = palette.to_css_vars(indent=2)

print(f".dracula {{\n{css_vars}\n}}")
```

Output:

```css
.dracula {
  --syntax-bg: #282a36;
  --syntax-bg-highlight: #44475a;
  --syntax-control: #ff79c6;
  --syntax-declaration: #8be9fd;
  --syntax-string: #f1fa8c;
  --syntax-number: #bd93f9;
  /* ... more variables */
}
```

Use these variables in your CSS:

```css
.syntax-keyword { color: var(--syntax-control); }
.syntax-function { color: var(--syntax-declaration); }
.syntax-string { color: var(--syntax-string); }
```

---

## Built-in Palettes

Rosettes includes these palettes:

| Name | Type | Description |
|------|------|-------------|
| `bengal-tiger` | Dark | Orange accent, high contrast |
| `bengal-snow-lynx` | Light | Teal accent, warm cream background |
| `bengal-charcoal` | Dark | Minimal, blue-purple tones |
| `bengal-blue` | Dark | Monochrome blue theme |
| `monokai` | Dark | Classic Sublime Text theme |
| `dracula` | Dark | Purple-accented dark theme |
| `github` | Adaptive | GitHub's light/dark theme |
| `github-light` | Light | GitHub light theme |
| `github-dark` | Dark | GitHub dark theme |

---

## Example: Brand-Aligned Palette

Create a palette matching your brand colors:

```python
from rosettes.themes import SyntaxPalette, register_palette

ACME_PALETTE = SyntaxPalette(
    name="acme",
    # Brand colors
    background="#0f172a",           # Slate 900
    text="#e2e8f0",                 # Slate 200
    
    # Primary: brand blue
    control_flow="#3b82f6",         # Blue 500
    declaration="#3b82f6",
    import_="#3b82f6",
    operator="#3b82f6",
    
    # Secondary: brand green
    string="#22c55e",               # Green 500
    function="#22c55e",
    added="#22c55e",
    
    # Accents
    number="#f59e0b",               # Amber 500
    constant="#f59e0b",
    warning="#f59e0b",
    
    type_="#a855f7",                # Purple 500
    attribute="#a855f7",
    
    # Neutral
    comment="#64748b",              # Slate 500
    muted="#64748b",
    punctuation="#94a3b8",          # Slate 400
    
    # Errors
    error="#ef4444",                # Red 500
    removed="#ef4444",
)

register_palette(ACME_PALETTE)
```

---

## Next Steps

- [[docs/styling/custom-themes|Custom Themes]] — CSS-based theming
- [[docs/styling/css-classes|CSS Classes]] — Full class reference
- [[docs/reference/token-types|Token Types]] — Token to role mappings

