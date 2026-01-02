---
title: Pygments Themes
description: Use existing Pygments themes with Rosettes
draft: false
weight: 20
lang: en
type: doc
tags:
- pygments
- themes
keywords:
- pygments
- themes
- monokai
- dracula
icon: palette
---

# Pygments Themes

Rosettes supports Pygments-compatible CSS classes, allowing you to use any existing Pygments theme.

## Enable Pygments Classes

```python
from rosettes import highlight

html = highlight(code, "python", css_class_style="pygments")
```

This generates HTML with Pygments class names:

```html
<div class="highlight" data-language="python">
  <pre><code><span class="k">def</span> <span class="nf">hello</span>...
```

## Using a Pygments Theme

### Option 1: CDN

Popular themes are available via CDN:

```html
<!-- Monokai -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/monokai.min.css">

<!-- Dracula -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/dracula.min.css">
```

:::{note}
highlight.js themes work with Pygments classes since they use the same class names.
:::

### Option 2: Generate from Pygments

If you have Pygments installed:

```bash
pygmentize -S monokai -f html > monokai.css
```

### Option 3: Copy a Theme

Here's Monokai as an example:

```css
.highlight { background: #272822; }
.highlight .c { color: #75715e } /* Comment */
.highlight .k { color: #66d9ef } /* Keyword */
.highlight .n { color: #f8f8f2 } /* Name */
.highlight .o { color: #f92672 } /* Operator */
.highlight .p { color: #f8f8f2 } /* Punctuation */
.highlight .s { color: #e6db74 } /* String */
.highlight .m { color: #ae81ff } /* Number */
.highlight .nf { color: #a6e22e } /* Name.Function */
.highlight .nc { color: #a6e22e } /* Name.Class */
.highlight .nd { color: #a6e22e } /* Name.Decorator */
.highlight .nb { color: #f8f8f2 } /* Name.Builtin */
```

---

## Popular Themes

| Theme | Style | Background |
|-------|-------|------------|
| Monokai | Dark | `#272822` |
| Dracula | Dark | `#282a36` |
| One Dark | Dark | `#282c34` |
| Solarized Dark | Dark | `#002b36` |
| Solarized Light | Light | `#fdf6e3` |
| GitHub | Light | `#ffffff` |
| GitHub Dark | Dark | `#0d1117` |

---

## Container Class

When using Pygments style, the container class changes:

```python
# Semantic style (default)
html = highlight(code, "python")
# <div class="rosettes">

# Pygments style
html = highlight(code, "python", css_class_style="pygments")
# <div class="highlight">

# Custom container
html = highlight(code, "python", css_class_style="pygments", css_class="codehilite")
# <div class="codehilite">
```

---

## Migration from Pygments

If you're switching from Pygments to Rosettes:

1. Keep your existing CSS theme
2. Use `css_class_style="pygments"`
3. No CSS changes needed

```python
# Before (Pygments)
from pygments import highlight as pyg_highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

html = pyg_highlight(code, PythonLexer(), HtmlFormatter())

# After (Rosettes)
from rosettes import highlight

html = highlight(code, "python", css_class_style="pygments")
```

---

## Next Steps

- [[docs/styling/custom-themes|Custom Themes]] — Build your own theme
- [[docs/tutorials/migrate-from-pygments|Migration Guide]] — Full migration walkthrough

