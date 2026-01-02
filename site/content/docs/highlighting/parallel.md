---
title: Parallel Processing
description: Highlight multiple code blocks concurrently with highlight_many()
draft: false
weight: 20
lang: en
type: doc
tags:
- parallel
- performance
keywords:
- highlight_many
- parallel
- concurrent
- free-threading
icon: cpu
---

# Parallel Processing

For sites with many code blocks, `highlight_many()` provides concurrent processing with 1.5-2x speedup on Python 3.14t.

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| < 8 blocks | Use `highlight()` in a loop |
| 8+ blocks | Use `highlight_many()` |
| 50+ blocks on 3.14t | Significant speedup |

The overhead of thread management makes `highlight_many()` slower for small batches. Rosettes automatically falls back to sequential processing for < 8 blocks.

---

## `highlight_many()`

Highlight multiple code blocks in parallel.

```python
from rosettes import highlight_many

blocks = [
    ("def foo(): pass", "python"),
    ("const x = 1;", "javascript"),
    ("fn main() {}", "rust"),
    ('{"key": "value"}', "json"),
]

results = highlight_many(blocks)
# Returns list of HTML strings in same order as input
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `Iterable[tuple[str, str]]` | required | (code, language) tuples |
| `max_workers` | `int` | `min(4, cpu_count)` | Thread count |
| `css_class_style` | `str` | `"semantic"` | `"semantic"` or `"pygments"` |

### Worker Count

The default of 4 workers is optimal based on benchmarking:

```python
# Default: 4 workers (optimal)
results = highlight_many(blocks)

# Custom worker count
results = highlight_many(blocks, max_workers=8)
```

:::{note}
More workers doesn't always mean faster. Thread overhead and memory contention can reduce performance beyond 4-8 workers.
:::

---

## `tokenize_many()`

Parallel tokenization for raw token access.

```python
from rosettes import tokenize_many

blocks = [
    ("x = 1", "python"),
    ("let y = 2;", "javascript"),
]

results = tokenize_many(blocks)
# Returns list of token lists

for i, tokens in enumerate(results):
    print(f"Block {i}: {len(tokens)} tokens")
```

---

## Free-Threading Performance

On Python 3.14t with free-threading enabled (PEP 703), `highlight_many()` provides true parallelism:

| Blocks | GIL Python | Free-Threading | Speedup |
|--------|------------|----------------|---------|
| 10 | 15ms | 12ms | 1.25x |
| 50 | 75ms | 42ms | 1.78x |
| 100 | 150ms | 78ms | 1.92x |

### Why It Works

Rosettes is thread-safe by design:

1. **Immutable tokens**: `Token` is a `NamedTuple`
2. **Local-only state**: Lexers use only local variables during tokenization
3. **No shared mutable data**: No global state to contend for
4. **PEP 703 declaration**: Module declares itself safe for free-threading

---

## Example: Static Site Generator

```python
from rosettes import highlight_many
from pathlib import Path

def highlight_all_code_blocks(pages: list[dict]) -> list[dict]:
    """Highlight all code blocks across all pages."""
    
    # Collect all code blocks
    blocks = []
    block_locations = []  # Track which page/block each belongs to
    
    for page_idx, page in enumerate(pages):
        for block_idx, block in enumerate(page["code_blocks"]):
            blocks.append((block["code"], block["language"]))
            block_locations.append((page_idx, block_idx))
    
    # Highlight in parallel
    results = highlight_many(blocks)
    
    # Assign results back to pages
    for (page_idx, block_idx), html in zip(block_locations, results):
        pages[page_idx]["code_blocks"][block_idx]["html"] = html
    
    return pages
```

---

## Next Steps

- [[docs/about/thread-safety|Thread Safety]] — How Rosettes achieves thread safety
- [[docs/about/performance|Performance]] — Benchmarks and optimization tips

