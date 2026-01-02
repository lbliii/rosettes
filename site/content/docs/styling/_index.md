---
title: Styling
description: CSS classes, themes, and visual customization
draft: false
weight: 30
lang: en
type: doc
cascade:
  type: doc
tags:
- styling
- css
- themes
keywords:
- css
- themes
- styling
- colors
icon: palette
---

# Styling

Rosettes generates semantic HTML with CSS classes for styling. Choose between readable semantic classes or Pygments-compatible classes for drop-in theme support.

## Two Class Styles

| Style | Classes | Use Case |
|-------|---------|----------|
| Semantic | `.syntax-keyword`, `.syntax-function` | Readable, self-documenting |
| Pygments | `.k`, `.nf` | Drop-in Pygments theme compatibility |

```python
# Semantic (default)
html = highlight(code, "python")
# <span class="syntax-keyword">def</span>

# Pygments-compatible
html = highlight(code, "python", css_class_style="pygments")
# <span class="k">def</span>
```

## Quick Start

Add this CSS to style semantic classes:

```css
/* Dark theme basics */
.rosettes {
  background: #282a36;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

.rosettes pre {
  margin: 0;
  font-family: 'Fira Code', monospace;
}

.syntax-keyword { color: #ff79c6; }
.syntax-function { color: #50fa7b; }
.syntax-string { color: #f1fa8c; }
.syntax-comment { color: #6272a4; }
.syntax-number { color: #bd93f9; }
```

## In This Section

:::{child-cards}
:columns: 1
:include: pages
:fields: title, description, icon
:::

