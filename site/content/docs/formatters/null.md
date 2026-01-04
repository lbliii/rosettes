---
title: Null Formatter
description: Raw, unformatted text output
draft: false
weight: 30
lang: en
type: doc
tags:
- null
- raw
keywords:
- null formatter
- raw text
- benchmarking
icon: blur_off
---

# Null Formatter

The Null Formatter yields raw, unformatted text.

## Usage

Use the `"null"` or `"none"` alias:

```python
from rosettes import highlight

code = "def hello(): pass"
raw = highlight(code, "python", formatter="null")

print(raw == code)  # True
```

## Why use a Null Formatter?

While it may seem counter-intuitive for a syntax highlighter, the Null Formatter is useful for:

1. **Benchmarking**: Measure the performance of lexers alone, excluding the overhead of HTML or ANSI formatting.
2. **Analysis**: Process code through the tokenization pipeline without generating a styled output.
3. **Fallback**: Provide a safe fallback when no highlighting is desired but you still want to use the `highlight()` API.
4. **Integration Testing**: Verify that the tokenization process doesn't lose or alter any characters from the source code.

## Performance

The Null Formatter uses the **Fast Path** exclusively, simply joining token values together. It is the fastest possible "formatting" path in Rosettes.

---

## Next Steps

- [[docs/formatters/terminal|Terminal Formatter]] — ANSI colors for consoles
- [[docs/formatters/html|HTML Formatter]] — Optimized HTML output

