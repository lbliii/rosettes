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

## What's good about it

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

| File Size | Time |
|-----------|------|
| ~50 lines | ~0.5ms |
| ~500 lines | ~5ms |
| 10,000 lines | ~220ms |

[Benchmark source](https://github.com/lbliii/rosettes/tree/main/benchmarks)

---

## The Bengal Ecosystem

A structured reactive stack — every layer written in pure Python for 3.14t free-threading.

| | | | |
|--:|---|---|---|
| **ᓚᘏᗢ** | [Bengal](https://github.com/lbliii/bengal) | Static site generator | [Docs](https://lbliii.github.io/bengal/) |
| **∿∿** | [Purr](https://github.com/lbliii/purr) | Content runtime | — |
| **⌁⌁** | [Chirp](https://github.com/lbliii/chirp) | Web framework | [Docs](https://lbliii.github.io/chirp/) |
| **=^..^=** | [Pounce](https://github.com/lbliii/pounce) | ASGI server | [Docs](https://lbliii.github.io/pounce/) |
| **)彡** | [Kida](https://github.com/lbliii/kida) | Template engine | [Docs](https://lbliii.github.io/kida/) |
| **ฅᨐฅ** | [Patitas](https://github.com/lbliii/patitas) | Markdown parser | [Docs](https://lbliii.github.io/patitas/) |
| **⌾⌾⌾** | **Rosettes** | Syntax highlighter ← You are here | [Docs](https://lbliii.github.io/rosettes/) |

Python-native. Free-threading ready. No npm required.
