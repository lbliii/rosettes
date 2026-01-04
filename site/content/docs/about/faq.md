---
title: FAQ
description: Frequently asked questions about Rosettes
draft: false
weight: 50
lang: en
type: doc
tags:
- faq
keywords:
- faq
- questions
- help
icon: info
---

# FAQ

## General

### What is Rosettes?

Rosettes is a pure-Python syntax highlighter designed for Python 3.14t's free-threading era. It uses hand-written state machine lexers instead of regex, guaranteeing O(n) performance and eliminating ReDoS vulnerabilities.

### Why "Rosettes"?

Rosettes are the distinctive rose-shaped spots on a Bengal cat's coat. This library was extracted from the [Bengal](https://github.com/lbliii/bengal) static site generator, maintaining the feline naming theme.

### What Python versions are supported?

Python 3.14 and later. Rosettes is designed for modern Python with free-threading support (PEP 703).

---

## Languages

### How many languages are supported?

55 languages including Python, JavaScript, TypeScript, Rust, Go, C, C++, Java, Ruby, PHP, and more.

### Why not 500+ languages like Pygments?

Quality over quantity. Each Rosettes lexer is a hand-written state machine optimized for performance and correctness. Adding a language requires careful implementation, not just regex patterns.

### Can I request a new language?

Yes! Open an issue on GitHub. Popular languages are prioritized.

### Does Rosettes support automatic language detection?

No. Rosettes requires explicit language specification. For auto-detection, use filename extensions or a separate library like `pygments.lexers.guess_lexer()`.

---

## Performance

### How much faster is Rosettes than Pygments?

2-4x faster for typical code blocks:

| Code Size | Speedup |
|-----------|---------|
| Medium (~50 lines) | 2-4x |
| Large (~500+ lines) | 3-5x |
| Parallel (8+ blocks) | Additional gains on 3.14t |

Run `python -m benchmarks.benchmark_vs_pygments` for your hardware.

### What is ReDoS and why should I care?

ReDoS (Regular Expression Denial of Service) occurs when a regex pattern exhibits exponential backtracking on certain inputs. A crafted string can freeze your application for hours.

Rosettes is immune to ReDoS because it doesn't use regex for lexing.

### When should I use `highlight_many()`?

For 8 or more code blocks. The thread pool overhead makes it slower for small batches.

---

## Styling

### Can I use my existing Pygments themes?

Yes! Use `css_class_style="pygments"`:

```python
html = highlight(code, "python", css_class_style="pygments")
```

### What's the difference between semantic and Pygments classes?

| Style | Example Class | Readable |
|-------|---------------|----------|
| Semantic | `.syntax-function` | ✅ Yes |
| Pygments | `.nf` | ❌ Cryptic |

Semantic classes are self-documenting. Pygments classes are compatible with existing themes.

---

## Integration

### Does Rosettes work with Sphinx?

Not directly. Sphinx uses Pygments. You'd need to build a Sphinx extension to use Rosettes.

### Does Rosettes work with Jupyter?

Not directly. Jupyter uses Pygments for syntax highlighting. Custom configuration would be needed.

### Does Rosettes work with Bengal?

Yes! Bengal uses Rosettes for all syntax highlighting.

---

## Thread Safety

### Is Rosettes thread-safe?

Yes. All public APIs are thread-safe:

- Tokens are immutable `NamedTuple`s
- Lexers use only local variables
- Registry uses `functools.cache`

### Does Rosettes work with Python 3.14t free-threading?

Yes. Rosettes declares itself safe for free-threading via `_Py_mod_gil` (PEP 703). The `highlight_many()` function provides true parallelism on 3.14t.

---

## Troubleshooting

### `LookupError: Unknown language`

The language name or alias isn't recognized:

```python
from rosettes import supports_language, list_languages

# Check if language is supported
supports_language("python")  # True
supports_language("cobol")   # False

# List all supported languages
print(list_languages())
```

### Output looks wrong

1. Check you're using the correct language
2. Verify your CSS includes the appropriate classes
3. Check for conflicting CSS rules

### Performance is slower than expected

1. Use `highlight_many()` for multiple blocks
2. Avoid `show_linenos=True` and `hl_lines` unless needed
3. Profile with `cProfile` to identify bottlenecks

---

## Contributing

### How do I add a new language?

1. Create `src/rosettes/lexers/mylang_sm.py` with a state machine lexer
2. Register in `src/rosettes/_registry.py`
3. Add tests in `tests/lexers/test_mylang.py`
4. Submit a pull request

### How do I report a bug?

Open an issue on GitHub with:

- Python version
- Rosettes version
- Minimal reproducing code
- Expected vs actual output

