---
title: Architecture
description: State machine lexer design and internals
draft: false
weight: 10
lang: en
type: doc
tags:
- architecture
- design
keywords:
- architecture
- state machine
- lexer
- design
icon: cpu
---

# Architecture

Rosettes uses hand-written state machine lexers instead of regular expressions. This design guarantees O(n) time complexity and eliminates ReDoS vulnerabilities.

## State Machine Lexers

Every lexer is a finite state machine that processes input character-by-character:

```
┌─────────────────────────────────────────────────────────────┐
│                    State Machine Lexer                       │
│                                                              │
│  ┌─────────┐   char    ┌─────────┐   char    ┌─────────┐   │
│  │ INITIAL │ ────────► │ STRING  │ ────────► │ ESCAPE  │   │
│  │ STATE   │           │ STATE   │           │ STATE   │   │
│  └─────────┘           └─────────┘           └─────────┘   │
│      │                      │                     │         │
│      │ emit                 │ emit                │ emit    │
│      ▼                      ▼                     ▼         │
│  [Token]               [Token]               [Token]        │
└─────────────────────────────────────────────────────────────┘
```

### Key Properties

| Property | Guarantee |
|----------|-----------|
| **Single-character lookahead** | O(n) time complexity |
| **No backtracking** | No ReDoS possible |
| **Immutable state** | Thread-safe |
| **Local variables only** | No shared mutable state |

---

## How It Works

### 1. Character-by-Character Processing

The lexer reads one character at a time, deciding what to do based on the current state and the character:

```python
def tokenize(self, code: str) -> Iterator[Token]:
    state = State.INITIAL
    pos = 0
    
    while pos < len(code):
        char = code[pos]
        
        if state == State.INITIAL:
            if char == '"':
                state = State.STRING
                start = pos
            elif char.isdigit():
                state = State.NUMBER
                start = pos
            # ... more transitions
        
        elif state == State.STRING:
            if char == '\\':
                state = State.ESCAPE
            elif char == '"':
                yield Token(TokenType.STRING, code[start:pos+1])
                state = State.INITIAL
        
        pos += 1
```

### 2. No Backtracking

Unlike regex engines that may backtrack on failed matches, state machines make irrevocable decisions:

```
Regex:      a+b  on "aaac"
            Tries: a, aa, aaa, then backtracks to try fewer a's
            
State Machine: 
            Reads 'a' → accumulate
            Reads 'a' → accumulate  
            Reads 'a' → accumulate
            Reads 'c' → emit NAME token, continue
            No backtracking needed
```

### 3. Predictable Performance

Because each character is processed exactly once, time complexity is always O(n):

| Input Size | Time (State Machine) | Time (Regex worst case) |
|------------|---------------------|-------------------------|
| 100 chars | 0.01ms | 0.01ms |
| 1,000 chars | 0.1ms | 0.1ms |
| 10,000 chars | 1ms | 1-10ms |
| 100,000 chars | 10ms | 10ms - ∞ (ReDoS) |

---

## Lexer Structure

Each lexer follows the same pattern:

```python
class PythonStateMachineLexer(StateMachineLexer):
    name = "python"
    aliases = ("py", "python3", "py3")
    
    def tokenize(
        self,
        code: str,
        config: LexerConfig | None = None,
        *,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]:
        # State machine implementation
        ...
    
    def tokenize_fast(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[tuple[TokenType, str]]:
        # Optimized path: yields (type, value) tuples without line tracking
        ...
```

### Two Tokenization Paths

| Method | Use Case | Features |
|--------|----------|----------|
| `tokenize()` | Line highlighting, analysis | Full line/column tracking |
| `tokenize_fast()` | Maximum performance | No line tracking |

The `highlight()` function automatically chooses the appropriate path based on options.

---

## Registry

Lexers are registered with their canonical name and aliases using a lazy-loading pattern:

```python
from dataclasses import dataclass
from functools import cache

@dataclass(frozen=True, slots=True)
class LexerSpec:
    """Specification for lazy-loading a lexer."""
    module: str
    class_name: str
    aliases: tuple[str, ...] = ()

# Static registry — lexers loaded on-demand
_LEXER_SPECS: dict[str, LexerSpec] = {
    "python": LexerSpec(
        "rosettes.lexers.python_sm",
        "PythonStateMachineLexer",
        aliases=("py", "python3", "py3"),
    ),
    "javascript": LexerSpec(
        "rosettes.lexers.javascript_sm",
        "JavaScriptStateMachineLexer",
        aliases=("js", "jsx"),
    ),
    # ...
}
```

The registry uses `functools.cache` for thread-safe memoization:

```python
def get_lexer(name: str) -> StateMachineLexer:
    """Get a lexer by name or alias. Cached for performance."""
    canonical = _normalize_name(name)
    return _get_lexer_by_canonical(canonical)

@cache
def _get_lexer_by_canonical(canonical: str) -> StateMachineLexer:
    """Internal cached loader - keyed by canonical name."""
    spec = _LEXER_SPECS[canonical]
    module = import_module(spec.module)
    lexer_class = getattr(module, spec.class_name)
    return lexer_class()
```

---

## Adding a New Lexer

To add a new language lexer:

1. Create `rosettes/lexers/mylang_sm.py` with a state machine class
2. Register in `rosettes/_registry.py` with a `LexerSpec` entry
3. Add tests in `tests/lexers/test_mylang.py`

Example minimal lexer:

```python
from collections.abc import Iterator

from rosettes._config import LexerConfig
from rosettes._types import Token, TokenType
from rosettes.lexers._state_machine import StateMachineLexer

class MyLangStateMachineLexer(StateMachineLexer):
    name = "mylang"
    aliases = ("ml",)
    
    def tokenize(
        self,
        code: str,
        config: LexerConfig | None = None,
        *,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]:
        if end is None:
            end = len(code)
        
        pos = start
        line = 1
        col = 1
        
        while pos < end:
            char = code[pos]
            # State machine logic here
            yield Token(TokenType.TEXT, char, line, col)
            pos += 1
            col += 1
    
    def tokenize_fast(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[tuple[TokenType, str]]:
        # Yields (type, value) tuples without line/col tracking
        if end is None:
            end = len(code)
        pos = start
        while pos < end:
            yield (TokenType.TEXT, code[pos])
            pos += 1
```

---

## Next Steps

- [[docs/about/thread-safety|Thread Safety]] — How thread safety is achieved
- [[docs/about/performance|Performance]] — Benchmarks and optimization

