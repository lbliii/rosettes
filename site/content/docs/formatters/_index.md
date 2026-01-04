---
title: Formatters
description: Output formatters for HTML, terminal, and more
draft: false
weight: 40
lang: en
type: doc
tags:
- formatters
- html
- terminal
keywords:
- formatters
- registry
- terminal
- html
- null
icon: format_paint
---

# Formatters

Rosettes supports multiple output formats through a modular formatter system.

## Available Formatters

Rosettes comes with three built-in formatters:

| Formatter | Alias | Output | Description |
|-----------|-------|--------|-------------|
| **HTML** | `html`, `htm` | HTML | Semantic or Pygments-compatible HTML |
| **Terminal** | `terminal`, `ansi` | ANSI | Colored text for command-line interfaces |
| **Null** | `null`, `none` | Raw | Unformatted text (useful for timing/analysis) |

## Using a Formatter

You can specify a formatter by name in the `highlight()` function:

```python
from rosettes import highlight

# Default is HTML
html = highlight(code, "python")

# Use terminal output
ansi = highlight(code, "python", formatter="terminal")

# Use raw output
raw = highlight(code, "python", formatter="null")
```

## Formatter Registry

Rosettes uses a registry system to manage formatters. You can list, check, and retrieve formatters dynamically.

### `list_formatters()`

List all supported formatter names:

```python
from rosettes import list_formatters

print(list_formatters())  # ['html', 'null', 'terminal']
```

### `supports_formatter()`

Check if a formatter is supported by name or alias:

```python
from rosettes import supports_formatter

supports_formatter("terminal")  # True
supports_formatter("ansi")      # True
supports_formatter("pdf")       # False
```

### `get_formatter()`

Retrieve a formatter instance:

```python
from rosettes import get_formatter

formatter = get_formatter("terminal")
print(formatter.name)  # 'terminal'
```

## Performance & Optimization

Built-in formatters are optimized for performance:
- **Fast Path**: When no line numbers or highlighting are needed, formatters use a zero-allocation path.
- **Pre-computation**: Static elements like ANSI codes or HTML spans are pre-computed at module load time.
- **Streaming**: Formatters yield chunks instead of building large strings in memory.

---

## Next Steps

- [[docs/formatters/html|HTML Formatter]] — Semantic and Pygments styling
- [[docs/formatters/terminal|Terminal Formatter]] — ANSI colors for consoles
- [[docs/formatters/null|Null Formatter]] — Raw text output
- [[docs/extending/custom-formatter|Custom Formatter]] — Build your own formatter

