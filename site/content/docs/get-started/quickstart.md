---
title: Quickstart
description: Highlight code in 2 minutes
draft: false
weight: 20
lang: en
type: doc
tags:
- quickstart
- tutorial
keywords:
- quickstart
- first steps
- hello world
icon: zap
---

# Quickstart

Highlight your first code block in under 2 minutes.

## 1. Install

```bash
pip install rosettes
```

## 2. Highlight Code

```python
from rosettes import highlight

code = '''
def greet(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"
'''

html = highlight(code, "python")
print(html)
```

Output:

```html
<div class="rosettes" data-language="python">
  <pre><code><span class="syntax-keyword">def</span> <span class="syntax-function">greet</span>...
```

## 3. Try Different Languages

```python
from rosettes import highlight

# JavaScript
js_html = highlight("const x = 42;", "javascript")

# Rust
rust_html = highlight("fn main() { println!(\"Hello\"); }", "rust")

# JSON
json_html = highlight('{"key": "value"}', "json")
```

## 4. Check Available Languages

```python
from rosettes import list_languages, supports_language

# List all 55 supported languages
print(list_languages())
# ['bash', 'c', 'clojure', 'cpp', 'css', ...]

# Check if a language is supported
print(supports_language("python"))  # True
print(supports_language("cobol"))   # False
```

## 5. Add Line Numbers

```python
html = highlight(code, "python", show_linenos=True)
```

## 6. Highlight Specific Lines

```python
html = highlight(code, "python", hl_lines={2, 3})
```

Lines 2 and 3 receive the `.hll` CSS class for highlighting.

## Next Steps

- [[docs/highlighting/basic-usage|Basic Usage]] — Full `highlight()` and `tokenize()` API
- [[docs/highlighting/parallel|Parallel Processing]] — Speed up with `highlight_many()`
- [[docs/styling/css-classes|CSS Classes]] — Style your highlighted code
- [[docs/reference/languages|Languages]] — All 55 supported languages

