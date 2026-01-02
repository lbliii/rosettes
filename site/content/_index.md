---
title: Rosettes
description: Modern syntax highlighting for Python 3.14t
template: home.html
weight: 100
type: page
draft: false
lang: en
keywords: [rosettes, syntax highlighting, python, free-threading, pygments]
category: home

# Hero configuration
blob_background: true

# CTA Buttons
cta_buttons:
  - text: Get Started
    url: /docs/get-started/
    style: primary
  - text: API Reference
    url: /docs/reference/api/
    style: secondary

show_recent_posts: false
---

## Syntax Highlighting, Reinvented

**O(n) guaranteed. Zero ReDoS. Thread-safe by design.**

Rosettes is a pure-Python syntax highlighter built for the free-threaded era. Every lexer is a hand-written state machine—no regex backtracking, no exponential blowup, no security vulnerabilities.

```python
from rosettes import highlight

html = highlight("def hello(): print('world')", "python")
```

---

## Why Rosettes?

:::{cards}
:columns: 2
:gap: medium

:::{card} O(n) Guaranteed
:icon: zap
Every lexer processes input in linear time. No regex patterns that can be exploited for denial-of-service attacks.
:::{/card}

:::{card} 55 Languages
:icon: code
Hand-written state machines for Python, JavaScript, Rust, Go, and 51 more languages. Full syntax support, not just keywords.
:::{/card}

:::{card} Free-Threading Ready
:icon: cpu
Optimized for Python 3.14t (PEP 703). True parallelism with `highlight_many()` for multi-core systems.
:::{/card}

:::{card} Pygments Compatible
:icon: palette
Drop-in CSS class compatibility. Use your existing Pygments themes or Rosettes' semantic classes.
:::{/card}

:::{/cards}

---

## Quick Example

```python
from rosettes import highlight, highlight_many

# Single block
html = highlight("const x = 1;", "javascript")

# Parallel processing (optimal for 8+ blocks)
blocks = [
    ("def foo(): pass", "python"),
    ("fn main() {}", "rust"),
    ("let x = 1;", "javascript"),
]
results = highlight_many(blocks)  # 1.5-2x speedup on 3.14t
```

---

## Performance

Benchmarked against Pygments ([source](https://github.com/lbliii/rosettes/tree/main/benchmarks)):

| File Size | Rosettes | Pygments | Speedup |
|-----------|----------|----------|---------|
| ~50 lines | 0.5ms | 1.5ms | 2.8x |
| ~500 lines | 5ms | 15ms | 3.2x |
| 10,000 lines | 220ms | 860ms | 3.9x |

