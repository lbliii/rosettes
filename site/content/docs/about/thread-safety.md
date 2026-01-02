---
title: Thread Safety
description: Thread-safe design and free-threading support
draft: false
weight: 20
lang: en
type: doc
tags:
- threading
- safety
keywords:
- thread safety
- free-threading
- PEP 703
- concurrent
icon: shield
---

# Thread Safety

Rosettes is thread-safe by design, with explicit support for Python 3.14t's free-threading mode (PEP 703).

## Thread-Safe Guarantees

All public APIs are safe for concurrent use:

| Component | Thread Safety Mechanism |
|-----------|------------------------|
| `highlight()` | Uses only local variables |
| `tokenize()` | Uses only local variables |
| `highlight_many()` | Thread pool with isolated workers |
| `Token` | Immutable `NamedTuple` |
| `get_lexer()` | `functools.cache` memoization |

---

## How It Works

### 1. Immutable Tokens

The `Token` type is a `NamedTuple`, which is immutable:

```python
class Token(NamedTuple):
    type: TokenType
    value: str
    line: int = 1
    column: int = 1
```

Tokens cannot be modified after creation, eliminating data races.

### 2. Local-Only Lexer State

Lexers use only local variables during tokenization:

```python
def tokenize(self, code: str) -> Iterator[Token]:
    # All state is local
    state = State.INITIAL
    pos = 0
    buffer = []
    
    while pos < len(code):
        # Process character
        ...
```

No instance variables or global state are modified during tokenization.

### 3. Cached Registry

The lexer registry uses `functools.cache`:

```python
@functools.cache
def get_lexer(name: str) -> Lexer:
    return LEXERS[name.lower()]()
```

This provides thread-safe memoization—the same lexer instance is returned for the same name across all threads.

### 4. Immutable Configuration

All configuration classes are frozen dataclasses:

```python
@dataclass(frozen=True)
class FormatConfig:
    css_class: str = "rosettes"
    data_language: str = ""
```

---

## Free-Threading Support (PEP 703)

Rosettes declares itself safe for free-threaded Python via the `_Py_mod_gil` attribute:

```python
def __getattr__(name: str) -> object:
    if name == "_Py_mod_gil":
        return 0  # Py_MOD_GIL_NOT_USED
    raise AttributeError(f"module 'rosettes' has no attribute {name!r}")
```

This tells Python 3.14t that Rosettes:
- Does not require the GIL
- Can run with true parallelism
- Is safe for concurrent access without locks

---

## Concurrent Usage Patterns

### Safe: Multiple Threads Highlighting

```python
from concurrent.futures import ThreadPoolExecutor
from rosettes import highlight

def highlight_page(content: str) -> str:
    # Extract and highlight all code blocks
    return highlight(content, "python")

with ThreadPoolExecutor(max_workers=4) as executor:
    pages = ["code1", "code2", "code3", "code4"]
    results = list(executor.map(highlight_page, pages))
```

### Safe: Shared Lexer Instance

```python
from rosettes import get_lexer

# Same instance returned (cached)
lexer = get_lexer("python")

# Safe to use from multiple threads
def process(code: str) -> list:
    return list(lexer.tokenize(code))
```

### Safe: highlight_many()

```python
from rosettes import highlight_many

# Designed for parallel execution
blocks = [(code, lang) for code, lang in code_blocks]
results = highlight_many(blocks)  # Thread pool internally
```

---

## What NOT to Do

### Don't: Modify Tokens

```python
# Tokens are immutable - this fails
token = Token(TokenType.KEYWORD, "def")
token.value = "class"  # ❌ AttributeError
```

### Don't: Rely on Global State

```python
# Don't do this - Rosettes has no global mutable state
import rosettes
rosettes.SOME_SETTING = True  # ❌ No effect, not supported
```

---

## Performance on 3.14t

On Python 3.14t with free-threading enabled, `highlight_many()` provides true parallelism:

| Scenario | GIL Python | Free-Threading | Speedup |
|----------|------------|----------------|---------|
| 10 blocks | 15ms | 12ms | 1.25x |
| 50 blocks | 75ms | 42ms | 1.78x |
| 100 blocks | 150ms | 78ms | 1.92x |

The speedup comes from true parallel execution without GIL contention.

---

## Verifying Free-Threading

Check if you're running free-threaded Python:

```python
import sys

if hasattr(sys, "_is_gil_enabled"):
    if sys._is_gil_enabled():
        print("GIL is enabled")
    else:
        print("Free-threading active!")
else:
    print("Python < 3.13 (always has GIL)")
```

---

## Next Steps

- [[docs/highlighting/parallel|Parallel Processing]] — Using `highlight_many()`
- [[docs/about/performance|Performance]] — Benchmarks and optimization

