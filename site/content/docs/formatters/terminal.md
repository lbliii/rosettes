---
title: Terminal Formatter
description: ANSI-colored output for command-line interfaces
draft: false
weight: 20
lang: en
type: doc
tags:
- terminal
- ansi
- console
keywords:
- terminal formatter
- ansi colors
- console output
icon: terminal
---

# Terminal Formatter

Generates ANSI-colored text for display in terminal consoles.

## Usage

Use the `"terminal"` or `"ansi"` alias in the `highlight()` function:

```python
from rosettes import highlight

code = "def hello(): print('world')"
ansi = highlight(code, "python", formatter="terminal")

print(ansi)  # Displays colored output in your terminal
```

## Features

- **ANSI Colors**: Uses standard 16-color ANSI escape sequences compatible with almost all terminal emulators.
- **High Performance**: Pre-computes escape sequences for all token types, ensuring the highlighting loop is as fast as possible.
- **Zero Configuration**: Automatically maps semantic roles to appropriate terminal colors.

## Color Mapping

The terminal formatter maps **Syntax Roles** to terminal colors:

| Role | Color |
|------|-------|
| Control Flow | Magenta |
| Declaration | Cyan |
| String | Green |
| Number | Yellow |
| Function | Blue |
| Comment | Gray |
| Error | Red |

## Thread-Safety

Like all Rosettes components, the `TerminalFormatter` is fully thread-safe and optimized for Python 3.14t free-threading. Each call uses only local state or immutable pre-computed tables.

---

## Next Steps

- [[docs/formatters/html|HTML Formatter]] — Output for web browsers
- [[docs/formatters/null|Null Formatter]] — Raw text output

