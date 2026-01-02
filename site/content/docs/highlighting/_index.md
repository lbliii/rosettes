---
title: Highlighting
description: Core highlighting APIs and patterns
draft: false
weight: 20
lang: en
type: doc
cascade:
  type: doc
tags:
- highlighting
- api
keywords:
- highlight
- tokenize
- syntax
icon: code
---

# Highlighting

Rosettes provides two core functions: `highlight()` for HTML output and `tokenize()` for raw tokens.

## Overview

| Function | Purpose | Returns |
|----------|---------|---------|
| `highlight()` | Generate HTML with syntax highlighting | `str` (HTML) |
| `tokenize()` | Get raw tokens for custom processing | `list[Token]` |
| `highlight_many()` | Parallel highlighting for multiple blocks | `list[str]` |
| `tokenize_many()` | Parallel tokenization | `list[list[Token]]` |

## Quick Example

```python
from rosettes import highlight, tokenize

# Get HTML output
html = highlight("def foo(): pass", "python")

# Get raw tokens
tokens = tokenize("def foo(): pass", "python")
for token in tokens:
    print(f"{token.type}: {token.value!r}")
```

## In This Section

:::{child-cards}
:columns: 1
:include: pages
:fields: title, description, icon
:::

