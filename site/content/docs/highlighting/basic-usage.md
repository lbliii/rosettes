---
title: Basic Usage
description: Using highlight() and tokenize() for syntax highlighting
draft: false
weight: 10
lang: en
type: doc
tags:
- highlighting
- api
keywords:
- highlight
- tokenize
- basic usage
icon: code
---

# Basic Usage

The two primary functions for syntax highlighting.

## `highlight()`

Generate HTML with syntax-highlighted code.

```python
from rosettes import highlight

html = highlight("def hello(): pass", "python")

# Use terminal output
ansi = highlight("def hello(): pass", "python", formatter="terminal")
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | required | Source code to highlight |
| `language` | `str` | required | Language name or alias |
| `formatter` | `str \| Formatter` | `"html"` | Formatter name or instance |
| `hl_lines` | `set[int]` | `None` | 1-based line numbers to highlight |
| `show_linenos` | `bool` | `False` | Include line numbers |
| `css_class` | `str` | `None` | Container CSS class (HTML only) |
| `css_class_style` | `str` | `"semantic"` | `"semantic"` or `"pygments"` (HTML only) |

### Language Aliases

Languages accept multiple aliases:

```python
# These are equivalent
highlight(code, "python")
highlight(code, "py")
highlight(code, "python3")

# JavaScript aliases
highlight(code, "javascript")
highlight(code, "js")
```

### CSS Class Styles

**Semantic** (default) — readable class names:

```python
html = highlight(code, "python")  # css_class_style="semantic"
# <span class="syntax-keyword">def</span>
# <span class="syntax-function">hello</span>
```

**Pygments** — compatible with Pygments themes:

```python
html = highlight(code, "python", css_class_style="pygments")
# <span class="k">def</span>
# <span class="nf">hello</span>
```

### Container Class

The output is wrapped in a container `<div>`:

```python
# Default: "rosettes" for semantic, "highlight" for pygments
html = highlight(code, "python")
# <div class="rosettes" data-language="python">...

html = highlight(code, "python", css_class_style="pygments")
# <div class="highlight" data-language="python">...

# Custom class
html = highlight(code, "python", css_class="my-code")
# <div class="my-code" data-language="python">...
```

---

## `tokenize()`

Get raw tokens without formatting. Useful for custom output formats or analysis.

```python
from rosettes import tokenize

tokens = tokenize("x = 42", "python")
for token in tokens:
    print(f"{token.type.name}: {token.value!r}")
```

Output:

```
NAME: 'x'
WHITESPACE: ' '
OPERATOR: '='
WHITESPACE: ' '
NUMBER_INTEGER: '42'
```

### Token Structure

Each token is a `NamedTuple` with:

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `TokenType` | Semantic token type |
| `value` | `str` | The actual text |
| `line` | `int` | 1-based line number |
| `column` | `int` | 1-based column number |

```python
token = tokens[0]
print(token.type)    # TokenType.NAME
print(token.value)   # 'x'
print(token.line)    # 1
print(token.column)  # 1
```

### Use Cases

- **Custom formatters**: Build terminal, LaTeX, or other output formats
- **Analysis**: Count tokens, find patterns, compute metrics
- **Testing**: Verify lexer behavior
- **Transformations**: Modify code based on token structure

---

## Error Handling

Both functions raise `LookupError` for unsupported languages:

```python
from rosettes import highlight, supports_language

# Check before highlighting
if supports_language("python"):
    html = highlight(code, "python")

# Or handle the exception
try:
    html = highlight(code, "unknown")
except LookupError as e:
    print(f"Unsupported language: {e}")
```

---

## Next Steps

- [[docs/highlighting/parallel|Parallel Processing]] — `highlight_many()` for multiple blocks
- [[docs/highlighting/line-highlighting|Line Highlighting]] — Highlight specific lines
- [[docs/styling/css-classes|CSS Classes]] — Style your output

