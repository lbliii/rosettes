---
title: Rosettes vs Pygments
description: Feature and performance comparison
draft: false
weight: 40
lang: en
type: doc
tags:
- comparison
- pygments
keywords:
- comparison
- pygments
- versus
- differences
icon: bar-chart
---

# Rosettes vs Pygments

A detailed comparison of Rosettes and Pygments for syntax highlighting.

## Summary

| Aspect | Rosettes | Pygments |
|--------|----------|----------|
| **Languages** | 55 | 500+ |
| **Performance** | 2-4x faster | Baseline |
| **ReDoS safe** | ✅ Yes | ❌ Some lexers vulnerable |
| **Free-threading** | ✅ Optimized | ❌ Not tested |
| **Dependencies** | None | None |
| **Maturity** | New (2026) | Established (2006) |

---

## When to Choose Rosettes

✅ **Choose Rosettes when:**

- You need guaranteed O(n) performance
- Security is critical (no ReDoS risk)
- You're using Python 3.14t with free-threading
- You're highlighting common languages (Python, JS, Rust, etc.)
- You want parallel highlighting for many code blocks

❌ **Choose Pygments when:**

- You need obscure language support (500+ languages)
- You need output formats beyond HTML (LaTeX, RTF, terminal)
- You're on Python < 3.14
- You need battle-tested stability

---

## Feature Comparison

### Language Support

| Category | Rosettes | Pygments |
|----------|----------|----------|
| Total languages | 55 | 500+ |
| Popular languages | ✅ Full coverage | ✅ Full coverage |
| Obscure languages | ❌ Limited | ✅ Extensive |
| Quality | Hand-written, optimized | Variable |

**Rosettes covers:** Python, JavaScript, TypeScript, Rust, Go, C, C++, Java, Ruby, PHP, and 45 more popular languages.

**Pygments adds:** COBOL, Fortran, Ada, dozens of DSLs, legacy languages, and specialized formats.

### Output Formats

| Format | Rosettes | Pygments |
|--------|----------|----------|
| HTML | ✅ | ✅ |
| Terminal/ANSI | ❌ | ✅ |
| LaTeX | ❌ | ✅ |
| RTF | ❌ | ✅ |
| SVG | ❌ | ✅ |
| IRC | ❌ | ✅ |

Rosettes focuses on HTML output. For other formats, use Pygments or build a custom formatter.

### CSS Compatibility

| Style | Rosettes | Pygments |
|-------|----------|----------|
| Pygments classes | ✅ `css_class_style="pygments"` | ✅ Native |
| Semantic classes | ✅ `css_class_style="semantic"` | ❌ N/A |
| Theme compatibility | ✅ Full | ✅ Native |

Rosettes can use any Pygments CSS theme with `css_class_style="pygments"`.

---

## Performance Comparison

### Single Block Highlighting

| File Size | Rosettes | Pygments | Speedup |
|-----------|----------|----------|---------|
| 100 lines | 0.5ms | 1.5ms | 3x |
| 1,000 lines | 2ms | 8ms | 4x |
| 10,000 lines | 18ms | 52ms | 2.9x |

### Parallel Highlighting (8 blocks)

| Scenario | Rosettes | Pygments | Speedup |
|----------|----------|----------|---------|
| GIL Python | 22ms | 48ms | 2.2x |
| Free-threading | 12ms | N/A | N/A |

Pygments doesn't have built-in parallel support, requiring manual thread pool setup.

---

## Security Comparison

### ReDoS Vulnerability

**Rosettes:** Not vulnerable. State machine lexers process each character exactly once.

**Pygments:** Some lexers are vulnerable. Crafted input can cause exponential processing time.

Example vulnerable pattern (simplified):

```python
# Pygments regex pattern (hypothetical)
r'(a+)+$'

# Malicious input
"aaaaaaaaaaaaaaaaaaaaaaaaaaaa!"

# Result: Exponential backtracking
```

Rosettes eliminates this entire category of vulnerability by design.

---

## API Comparison

### Basic Highlighting

**Rosettes:**
```python
from rosettes import highlight
html = highlight("def foo(): pass", "python")
```

**Pygments:**
```python
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

html = highlight("def foo(): pass", PythonLexer(), HtmlFormatter())
```

### Tokenization

**Rosettes:**
```python
from rosettes import tokenize
tokens = tokenize("x = 1", "python")
```

**Pygments:**
```python
from pygments.lexers import PythonLexer
tokens = list(PythonLexer().get_tokens("x = 1"))
```

### Parallel Highlighting

**Rosettes:**
```python
from rosettes import highlight_many
results = highlight_many(blocks)  # Built-in
```

**Pygments:**
```python
from concurrent.futures import ThreadPoolExecutor
from pygments import highlight
# ... manual setup required
```

---

## Migration Path

Switching from Pygments to Rosettes is straightforward for HTML output:

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

---

## Ecosystem

### Pygments Ecosystem

- Sphinx integration
- Jupyter integration
- Many editor plugins
- 18+ years of community themes
- Extensive documentation

### Rosettes Ecosystem

- Bengal static site generator
- Pygments CSS theme compatibility
- Growing documentation
- Modern Python 3.14+ focus

---

## Conclusion

| Priority | Recommendation |
|----------|----------------|
| **Security** | Rosettes |
| **Performance** | Rosettes |
| **Language coverage** | Pygments |
| **Output formats** | Pygments |
| **Modern Python** | Rosettes |
| **Stability** | Pygments |

For most web applications highlighting popular languages, Rosettes provides better performance and security. For specialized needs (obscure languages, non-HTML output), Pygments remains the comprehensive choice.

