---
title: Configuration
description: Configuration classes and options
draft: false
weight: 40
lang: en
type: doc
tags:
- configuration
- reference
keywords:
- configuration
- options
- settings
icon: settings
---

# Configuration

Rosettes uses immutable dataclasses for configuration. All configuration is optional—sensible defaults are provided.

## FormatConfig

Configuration for HTML output formatting.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FormatConfig:
    css_class: str = "rosettes"
    data_language: str = ""
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `css_class` | `str` | `"rosettes"` | Container `<div>` CSS class |
| `data_language` | `str` | `""` | Value for `data-language` attribute |

### Example

```python
from rosettes.formatters import HtmlFormatter
from rosettes import get_lexer, FormatConfig

lexer = get_lexer("python")
formatter = HtmlFormatter()

config = FormatConfig(
    css_class="my-code-block",
    data_language="python",
)

tokens = lexer.tokenize("x = 1")
html = formatter.format_string(tokens, config)
# <div class="my-code-block" data-language="python">...
```

---

## HighlightConfig

Configuration for line highlighting and line numbers.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class HighlightConfig:
    hl_lines: frozenset[int] = frozenset()
    show_linenos: bool = False
    css_class: str = "rosettes"
```

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `hl_lines` | `frozenset[int]` | `frozenset()` | 1-based line numbers to highlight |
| `show_linenos` | `bool` | `False` | Include line numbers in output |
| `css_class` | `str` | `"rosettes"` | Container CSS class |

### Example

```python
from rosettes import HighlightConfig
from rosettes.formatters import HtmlFormatter

config = HighlightConfig(
    hl_lines=frozenset({2, 3}),
    show_linenos=True,
)

formatter = HtmlFormatter(config=config)
```

---

## LexerConfig

Configuration for lexer behavior (rarely needed).

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class LexerConfig:
    pass  # Reserved for future lexer options
```

Currently empty—reserved for future lexer-specific options.

---

## High-Level API Defaults

The `highlight()` function uses these defaults:

| Parameter | Default | Derived From |
|-----------|---------|--------------|
| `css_class` | `"rosettes"` (semantic) or `"highlight"` (pygments) | `css_class_style` |
| `css_class_style` | `"semantic"` | |
| `show_linenos` | `False` | |
| `hl_lines` | `None` | |

```python
# These are equivalent
highlight(code, "python")
highlight(
    code,
    "python",
    hl_lines=None,
    show_linenos=False,
    css_class=None,  # Auto: "rosettes"
    css_class_style="semantic",
)
```

---

## Immutability

All configuration classes are frozen dataclasses:

```python
from rosettes import FormatConfig

config = FormatConfig(css_class="code")

# This raises FrozenInstanceError
config.css_class = "other"  # ❌ Error

# Create a new instance instead
new_config = FormatConfig(css_class="other")  # ✅
```

This immutability ensures thread safety.

---

## Environment Variables

Rosettes does not read environment variables. All configuration is explicit through function parameters or configuration classes.

For build-time configuration in static site generators, pass options through your build system:

```python
import os
from rosettes import highlight

CSS_STYLE = os.getenv("ROSETTES_CSS_STYLE", "semantic")

def highlight_code(code: str, language: str) -> str:
    return highlight(code, language, css_class_style=CSS_STYLE)
```

