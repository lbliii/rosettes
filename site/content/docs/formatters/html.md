---
title: HTML Formatter
description: High-performance HTML output with semantic or Pygments styling
draft: false
weight: 10
lang: en
type: doc
tags:
- html
- formatter
keywords:
- html formatter
- semantic
- pygments
icon: html
---

# HTML Formatter

The default formatter for Rosettes, generating optimized HTML output.

## Usage

The HTML formatter is used by default if no `formatter` is specified:

```python
from rosettes import highlight

html = highlight(code, "python")
# or explicitly:
html = highlight(code, "python", formatter="html")
```

## Styling Modes

The HTML formatter supports two different CSS class naming styles via the `css_class_style` parameter.

### Semantic Style (Default)

Uses readable, semantic class names (e.g., `.syntax-function`, `.syntax-keyword`).

```python
html = highlight(code, "python", css_class_style="semantic")
# Output: <span class="syntax-keyword">def</span>
```

### Pygments Style

Uses short, Pygments-compatible class names (e.g., `.nf`, `.k`). This allows you to use existing Pygments CSS themes.

```python
html = highlight(code, "python", css_class_style="pygments")
# Output: <span class="k">def</span>
```

## Advanced Configuration

You can pass a custom `HtmlFormatter` instance to control internal behavior:

```python
from rosettes import highlight
from rosettes.formatters import HtmlFormatter
from rosettes import HighlightConfig

# Custom configuration
config = HighlightConfig(
    hl_lines={1, 2},
    hl_line_class="my-highlight",
    lineno_class="my-lineno"
)

formatter = HtmlFormatter(config=config, css_class_style="pygments")
html = highlight(code, "python", formatter=formatter)
```

## Optimizations

The HTML formatter is designed for maximum speed:
1. **Pre-built Templates**: HTML span tags for all token types are pre-computed.
2. **Fast Path**: Uses a specialized zero-allocation loop when line highlighting is disabled.
3. **Translates**: Uses C-optimized `str.translate` for HTML escaping.

---

## Next Steps

- [[docs/styling/css-classes|CSS Classes]] — Reference for available classes
- [[docs/styling/pygments-themes|Pygments Themes]] — Using external CSS

