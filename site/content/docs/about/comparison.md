---
title: Choosing Rosettes
description: When Rosettes fits and what it offers
draft: false
weight: 40
lang: en
type: doc
tags:
- choosing
- features
keywords:
- choosing
- features
- migration
icon: bar-chart
---

# Choosing Rosettes

Rosettes is a good fit when you need syntax highlighting with predictable performance and security.

## What Rosettes Offers

- **O(n) guaranteed** — State machine lexers, no regex backtracking
- **ReDoS safe** — Safe for untrusted input in web apps and APIs
- **55 languages** — Python, JavaScript, Rust, Go, and other popular languages
- **Free-threading ready** — Optimized for Python 3.14t
- **Parallel highlighting** — `highlight_many()` for multiple blocks
- **Zero dependencies** — Pure Python
- **Pygments CSS compatibility** — Use existing themes with `css_class_style="pygments"`

## When Rosettes Fits

- Web applications highlighting user code or documentation
- Static site generators (e.g., Bengal)
- Python 3.14+ projects using free-threading
- Projects where security and predictable performance matter

## Limitations

- **55 languages** — Covers popular languages; not the 500+ that some tools support
- **HTML and terminal output** — No built-in LaTeX, RTF, or SVG formatters
- **Python 3.14+** — Requires modern Python

## Migration from Pygments

Switching to Rosettes is straightforward for HTML output:

```python
# Before (Pygments)
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

lexer = get_lexer_by_name("python")
formatter = HtmlFormatter()
html = highlight(code, lexer, formatter)

# After (Rosettes)
from rosettes import highlight

html = highlight(code, "python", css_class_style="pygments")
```

Your existing CSS themes work without changes.

See [[docs/tutorials/migrate-from-pygments|Migration Guide]] for a complete walkthrough.
