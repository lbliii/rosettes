---
title: API Reference
description: Complete API documentation with signatures and examples
draft: false
weight: 10
lang: en
type: doc
tags:
- api
- reference
keywords:
- api
- functions
- highlight
- tokenize
icon: code
---

# API Reference

Complete reference for all public functions and classes.

## High-Level Functions

### `highlight()`

Highlight source code and return HTML.

```python
def highlight(
    code: str,
    language: str,
    *,
    hl_lines: set[int] | frozenset[int] | None = None,
    show_linenos: bool = False,
    css_class: str | None = None,
    css_class_style: str = "semantic",
    start: int = 0,
    end: int | None = None,
) -> str: ...
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | required | Source code to highlight |
| `language` | `str` | required | Language name or alias |
| `hl_lines` | `set[int] \| None` | `None` | 1-based line numbers to highlight |
| `show_linenos` | `bool` | `False` | Include line numbers in output |
| `css_class` | `str \| None` | `None` | Container CSS class (auto-detected from style) |
| `css_class_style` | `str` | `"semantic"` | `"semantic"` or `"pygments"` |
| `start` | `int` | `0` | Starting index in source string |
| `end` | `int \| None` | `None` | Ending index in source string |

**Returns:** HTML string with syntax-highlighted code.

**Raises:** `LookupError` if language is not supported.

**Example:**

```python
from rosettes import highlight

# Basic usage
html = highlight("def foo(): pass", "python")

# With line highlighting
html = highlight(code, "python", hl_lines={2, 3}, show_linenos=True)

# Pygments-compatible output
html = highlight(code, "python", css_class_style="pygments")
```

---

### `tokenize()`

Tokenize source code without formatting.

```python
def tokenize(
    code: str,
    language: str,
    start: int = 0,
    end: int | None = None,
) -> list[Token]: ...
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `str` | required | Source code to tokenize |
| `language` | `str` | required | Language name or alias |
| `start` | `int` | `0` | Starting index in source string |
| `end` | `int \| None` | `None` | Ending index in source string |

**Returns:** List of `Token` objects.

**Raises:** `LookupError` if language is not supported.

**Example:**

```python
from rosettes import tokenize

tokens = tokenize("x = 42", "python")
for token in tokens:
    print(f"{token.type.name}: {token.value!r}")
```

---

## Parallel Functions

### `highlight_many()`

Highlight multiple code blocks in parallel.

```python
def highlight_many(
    items: Iterable[tuple[str, str]],
    *,
    max_workers: int | None = None,
    css_class_style: str = "semantic",
) -> list[str]: ...
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `Iterable[tuple[str, str]]` | required | (code, language) tuples |
| `max_workers` | `int \| None` | `min(4, cpu_count)` | Thread count |
| `css_class_style` | `str` | `"semantic"` | Class style for all blocks |

**Returns:** List of HTML strings in same order as input.

**Example:**

```python
from rosettes import highlight_many

blocks = [
    ("def foo(): pass", "python"),
    ("const x = 1;", "javascript"),
]
results = highlight_many(blocks)
```

---

### `tokenize_many()`

Tokenize multiple code blocks in parallel.

```python
def tokenize_many(
    items: Iterable[tuple[str, str]],
    *,
    max_workers: int | None = None,
) -> list[list[Token]]: ...
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `Iterable[tuple[str, str]]` | required | (code, language) tuples |
| `max_workers` | `int \| None` | `min(4, cpu_count)` | Thread count |

**Returns:** List of token lists in same order as input.

---

## Registry Functions

### `get_lexer()`

Get a lexer instance by name or alias.

```python
def get_lexer(name: str) -> Lexer: ...
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Language name or alias |

**Returns:** Lexer instance.

**Raises:** `LookupError` if language is not supported.

**Example:**

```python
from rosettes import get_lexer

lexer = get_lexer("python")
tokens = list(lexer.tokenize("x = 1"))
```

---

### `list_languages()`

List all supported language names.

```python
def list_languages() -> list[str]: ...
```

**Returns:** Sorted list of canonical language names.

**Example:**

```python
from rosettes import list_languages

languages = list_languages()
print(len(languages))  # 55
print(languages[:5])   # ['bash', 'c', 'clojure', 'cpp', 'css']
```

---

### `supports_language()`

Check if a language is supported.

```python
def supports_language(name: str) -> bool: ...
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Language name or alias to check |

**Returns:** `True` if supported, `False` otherwise.

**Example:**

```python
from rosettes import supports_language

supports_language("python")  # True
supports_language("py")      # True (alias)
supports_language("cobol")   # False
```

---

## Types

### `Token`

Immutable token representing a piece of highlighted code.

```python
class Token(NamedTuple):
    type: TokenType
    value: str
    line: int = 1
    column: int = 1
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | `TokenType` | Semantic token type |
| `value` | `str` | The actual text content |
| `line` | `int` | 1-based line number |
| `column` | `int` | 1-based column number |

---

### `TokenType`

Enumeration of all token types. See [[docs/reference/token-types|Token Types]] for complete list.

```python
class TokenType(StrEnum):
    KEYWORD = "k"
    NAME = "n"
    STRING = "s"
    # ... 60+ types
```

---

## Protocols

### `Lexer`

Protocol for lexer implementations.

```python
class Lexer(Protocol):
    name: str
    aliases: tuple[str, ...]
    
    def tokenize(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]: ...
    
    def tokenize_fast(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]: ...
```

---

### `Formatter`

Protocol for formatter implementations.

```python
class Formatter(Protocol):
    def format_string(
        self,
        tokens: Iterable[Token],
        config: FormatConfig,
    ) -> str: ...
```

---

## Configuration Classes

### `FormatConfig`

Configuration for HTML output.

```python
@dataclass(frozen=True)
class FormatConfig:
    css_class: str = "rosettes"
    data_language: str = ""
```

### `HighlightConfig`

Configuration for line highlighting.

```python
@dataclass(frozen=True)
class HighlightConfig:
    hl_lines: frozenset[int] = frozenset()
    show_linenos: bool = False
    css_class: str = "rosettes"
```

---

## Module Attributes

### `__version__`

Current version string.

```python
from rosettes import __version__
print(__version__)  # "0.3.0"
```

