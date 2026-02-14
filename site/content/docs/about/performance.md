---
title: Performance
description: Benchmarks and performance characteristics
draft: false
weight: 30
lang: en
type: doc
tags:
- performance
- benchmarks
keywords:
- performance
- benchmarks
- speed
- optimization
icon: zap
---

# Performance

Rosettes is designed for predictable, high performance. State machine lexers provide O(n) time complexity with no worst-case surprises.

## Benchmarks

Tested on a 10,000-line Python file:

| Operation | Time |
|-----------|------|
| Tokenize | 12ms |
| Highlight | 18ms |
| Parallel (8 blocks) | 22ms |

*Benchmarked on Apple M1 Pro, Python 3.14. Results vary by hardware—run `python -m benchmarks.benchmark_vs_pygments` to measure on your system.*

---

## Time Complexity

### O(n) Guaranteed

Rosettes processes each character exactly once:

| Input Size | Time |
|------------|------|
| 1,000 chars | ~0.1ms |
| 10,000 chars | ~1ms |
| 100,000 chars | ~10ms |
| 1,000,000 chars | ~100ms |

Linear scaling—no exponential blowup.

### Why State Machines?

Regex-based parsing can exhibit catastrophic backtracking:

```
Pattern: (a+)+$
Input:   "aaaaaaaaaaaaaaaaaaaaaaaaaaaa!"

Regex:   Exponential time (2^n attempts)
Rosettes: Linear time (n character reads)
```

---

## Memory Usage

Rosettes uses minimal memory:

| Component | Memory |
|-----------|--------|
| Lexer instance | ~1 KB |
| Token | 72 bytes |
| 10,000 tokens | ~720 KB |

Tokens are `NamedTuple`s—lightweight and cache-friendly.

---

## Optimization Tips

### Use `highlight_many()` for Multiple Blocks

For 8+ code blocks, parallel processing is faster:

```python
# Slow: sequential
results = [highlight(code, lang) for code, lang in blocks]

# Fast: parallel (for 8+ blocks)
results = highlight_many(blocks)
```

| Blocks | Sequential | Parallel | Speedup |
|--------|------------|----------|---------|
| 4 | 10ms | 12ms | 0.83x (overhead) |
| 8 | 20ms | 15ms | 1.33x |
| 50 | 125ms | 70ms | 1.79x |
| 100 | 250ms | 130ms | 1.92x |

### Skip Line Features When Not Needed

Line numbers and line highlighting use the slower code path:

```python
# Fast path (no line features)
html = highlight(code, "python")

# Slow path (line features enabled)
html = highlight(code, "python", show_linenos=True)
html = highlight(code, "python", hl_lines={1, 2, 3})
```

The difference is ~15% for typical code blocks.

### Reuse Lexer Instances

Lexers are cached automatically:

```python
from rosettes import get_lexer

# Same instance returned (cached)
lexer1 = get_lexer("python")
lexer2 = get_lexer("python")
assert lexer1 is lexer2  # True
```

No need to manually cache lexers.

---

## Parallel Scaling

### GIL Python (3.13 and earlier)

With the GIL, parallel highlighting provides limited benefit:

| Workers | Speedup |
|---------|---------|
| 1 | 1.0x |
| 2 | 1.1x |
| 4 | 1.15x |
| 8 | 1.2x |

The GIL prevents true parallelism, but I/O overlapping provides some benefit.

### Free-Threading (3.14t)

With free-threading enabled, true parallelism is achieved:

| Workers | Speedup |
|---------|---------|
| 1 | 1.0x |
| 2 | 1.8x |
| 4 | 3.2x |
| 8 | 4.5x |

Near-linear scaling up to 4 workers, then diminishing returns due to memory bandwidth.

---

## Profiling

Profile your highlighting with `cProfile`:

```python
import cProfile
from rosettes import highlight

code = open("large_file.py").read()

cProfile.run('highlight(code, "python")', sort="cumtime")
```

Or use `timeit` for quick benchmarks:

```python
import timeit
from rosettes import highlight

code = "def foo(): pass\n" * 10000

time = timeit.timeit(
    lambda: highlight(code, "python"),
    number=100,
)
print(f"Average: {time/100*1000:.2f}ms")
```

---

## Characteristics

| Feature | Rosettes |
|---------|----------|
| Time complexity | O(n) guaranteed |
| ReDoS vulnerable | No |
| Parallel support | Native `highlight_many()` |
| Free-threading | Optimized |
| Memory per token | 72 bytes |
| Dependencies | None |

---

## Next Steps
- [[docs/highlighting/parallel|Parallel Processing]] — Using `highlight_many()`

