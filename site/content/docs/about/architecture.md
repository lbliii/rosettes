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
class PythonLexer:
    name = "python"
    aliases = ("py", "python3")
    
    def tokenize(self, code: str, start: int = 0, end: int | None = None) -> Iterator[Token]:
        # State machine implementation
        ...
    
    def tokenize_fast(self, code: str, start: int = 0, end: int | None = None) -> Iterator[Token]:
        # Optimized path without line tracking
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

Lexers are registered with their canonical name and aliases:

```python
# Internal registry structure
LEXERS = {
    "python": PythonLexer,
    "py": PythonLexer,      # alias
    "python3": PythonLexer, # alias
    "javascript": JavaScriptLexer,
    "js": JavaScriptLexer,  # alias
    # ...
}
```

The registry uses `functools.cache` for thread-safe memoization:

```python
@functools.cache
def get_lexer(name: str) -> Lexer:
    lexer_class = LEXERS.get(name.lower())
    if lexer_class is None:
        raise LookupError(f"Unknown language: {name}")
    return lexer_class()
```

---

## Adding a New Lexer

To add a new language lexer:

1. Create `lexers/mylang_sm.py` with a state machine class
2. Register in `lexers/__init__.py`
3. Add tests in `tests/lexers/test_mylang.py`

Example minimal lexer:

```python
from rosettes._types import Token, TokenType

class MyLangLexer:
    name = "mylang"
    aliases = ("ml",)
    
    def tokenize(self, code: str, start: int = 0, end: int | None = None) -> Iterator[Token]:
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
    
    def tokenize_fast(self, code: str, start: int = 0, end: int | None = None) -> Iterator[Token]:
        # Same as tokenize but without line/col tracking
        yield from self.tokenize(code, start, end)
```

---

## Next Steps

- [[docs/about/thread-safety|Thread Safety]] — How thread safety is achieved
- [[docs/about/performance|Performance]] — Benchmarks and optimization

