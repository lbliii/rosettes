---
title: Line Highlighting
description: Highlight specific lines and add line numbers
draft: false
weight: 30
lang: en
type: doc
tags:
- highlighting
- lines
keywords:
- hl_lines
- line numbers
- show_linenos
icon: list
---

# Line Highlighting

Draw attention to specific lines or add line numbers to code blocks.

## Highlight Specific Lines

Use `hl_lines` to highlight specific lines:

```python
from rosettes import highlight

code = '''def greet(name):
    message = f"Hello, {name}!"
    return message
'''

# Highlight line 2 (1-based indexing)
html = highlight(code, "python", hl_lines={2})
```

The highlighted line receives the `.hll` CSS class:

```html
<div class="rosettes" data-language="python">
  <pre><code>
    <span class="line">def greet(name):</span>
    <span class="line hll">    message = f"Hello, {name}!"</span>
    <span class="line">    return message</span>
  </code></pre>
</div>
```

### Multiple Lines

Pass a set of line numbers:

```python
# Highlight lines 2 and 3
html = highlight(code, "python", hl_lines={2, 3})

# Highlight a range
html = highlight(code, "python", hl_lines=set(range(2, 5)))  # lines 2, 3, 4
```

### Styling Highlighted Lines

```css
/* Subtle background highlight */
.rosettes .hll {
  background-color: rgba(255, 255, 0, 0.1);
  display: block;
}

/* Or with a border */
.rosettes .hll {
  border-left: 3px solid #f1fa8c;
  padding-left: 0.5em;
  margin-left: -0.5em;
}
```

---

## Line Numbers

Add line numbers with `show_linenos`:

```python
html = highlight(code, "python", show_linenos=True)
```

Output structure:

```html
<div class="rosettes" data-language="python">
  <pre><code>
    <span class="lineno">1</span><span class="line">def greet(name):</span>
    <span class="lineno">2</span><span class="line">    message = f"Hello, {name}!"</span>
    <span class="lineno">3</span><span class="line">    return message</span>
  </code></pre>
</div>
```

### Styling Line Numbers

```css
.rosettes .lineno {
  color: #6272a4;
  user-select: none;  /* Don't include in copy */
  padding-right: 1em;
  text-align: right;
  min-width: 2em;
  display: inline-block;
}
```

---

## Combining Options

Use both together:

```python
html = highlight(
    code,
    "python",
    show_linenos=True,
    hl_lines={2, 3},
)
```

---

## Performance Note

Line highlighting and line numbers use the "slow path" internally, which processes tokens line-by-line. For maximum performance without these features, the "fast path" streams tokens directly.

| Mode | Use Case | Relative Speed |
|------|----------|----------------|
| Fast path | No line features | 1.0x |
| Slow path | `hl_lines` or `show_linenos` | ~0.85x |

The difference is negligible for most use cases.

---

## Next Steps

- [[docs/styling/css-classes|CSS Classes]] — Full list of CSS classes
- [[docs/highlighting/basic-usage|Basic Usage]] — Core `highlight()` API

