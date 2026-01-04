---
title: Custom Formatter
description: Build custom output formats beyond HTML
draft: false
weight: 10
lang: en
type: doc
tags:
- formatter
- customization
keywords:
- custom formatter
- terminal
- latex
icon: code
---

# Custom Formatter

Build custom formatters for terminal output, LaTeX, or any other format.

## The Formatter Protocol

Formatters implement the `Formatter` protocol defined in `rosettes._protocol`:

```python
from collections.abc import Iterator
from typing import Protocol
from rosettes import Token, TokenType, FormatConfig

class Formatter(Protocol):
    @property
    def name(self) -> str:
        """Canonical formatter name (e.g., 'html', 'terminal')."""
        ...

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Stream formatted output from full Token objects."""
        ...

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Stream formatted output from (type, value) tuples.
        
        Used by the fast path when line numbers aren't needed.
        """
        ...

    def format_string(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> str:
        """Format tokens and return as a single string."""
        ...

    def format_string_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> str:
        """Fast format and return as a single string."""
        ...
```

All four methods are required. The `format_string*` methods are typically implemented as:

```python
def format_string(self, tokens, config=None):
    return "".join(self.format(tokens, config))

def format_string_fast(self, tokens, config=None):
    return "".join(self.format_fast(tokens, config))
```

## Example: Simple ANSI Formatter

A minimal formatter that outputs ANSI-colored terminal text:

```python
from collections.abc import Iterator
from dataclasses import dataclass
from rosettes import tokenize, Token, TokenType, FormatConfig

# ANSI color codes
COLORS = {
    TokenType.KEYWORD: "\033[95m",       # Magenta
    TokenType.NAME_FUNCTION: "\033[92m", # Green
    TokenType.STRING: "\033[93m",        # Yellow
}
RESET = "\033[0m"


@dataclass(frozen=True, slots=True)
class SimpleAnsiFormatter:
    """Thread-safe ANSI formatter using frozen dataclass."""

    @property
    def name(self) -> str:
        return "simple-ansi"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        for token in tokens:
            color = COLORS.get(token.type, "")
            if color:
                yield f"{color}{token.value}{RESET}"
            else:
                yield token.value

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        for tt, value in tokens:
            color = COLORS.get(tt, "")
            if color:
                yield f"{color}{value}{RESET}"
            else:
                yield value

    def format_string(self, tokens, config=None):
        return "".join(self.format(tokens, config))

    def format_string_fast(self, tokens, config=None):
        return "".join(self.format_fast(tokens, config))


# Usage with highlight()
from rosettes import highlight

formatter = SimpleAnsiFormatter()
output = highlight("x = 1", "python", formatter=formatter)
```

Rosettes includes a full-featured `TerminalFormatter` with semantic role mapping — see [[docs/formatters/terminal|Terminal Formatter]].

## Example: Markdown Formatter

A formatter that outputs fenced code blocks:

```python
from collections.abc import Iterator
from dataclasses import dataclass
from rosettes import Token, TokenType, FormatConfig


@dataclass(frozen=True, slots=True)
class MarkdownFormatter:
    """Wraps code in a fenced markdown block."""

    @property
    def name(self) -> str:
        return "markdown"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        lang = config.data_language if config else ""
        yield f"```{lang}\n"
        for token in tokens:
            yield token.value
        yield "\n```"

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        lang = config.data_language if config else ""
        yield f"```{lang}\n"
        for _, value in tokens:
            yield value
        yield "\n```"

    def format_string(self, tokens, config=None):
        return "".join(self.format(tokens, config))

    def format_string_fast(self, tokens, config=None):
        return "".join(self.format_fast(tokens, config))


# Usage
from rosettes import highlight

output = highlight("x = 1", "python", formatter=MarkdownFormatter())
# ```python
# x = 1
# ```
```

## Example: JSON Token Dump

Export tokens as JSON for analysis:

```python
import json
from collections.abc import Iterator
from dataclasses import dataclass
from rosettes import Token, TokenType, FormatConfig


@dataclass(frozen=True, slots=True)
class JsonFormatter:
    """Exports tokens as a JSON array."""

    @property
    def name(self) -> str:
        return "json"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        # Collect tokens for JSON serialization
        token_list = [
            {
                "type": token.type.name,
                "value": token.value,
                "line": token.line,
                "column": token.column,
            }
            for token in tokens
        ]
        yield json.dumps(token_list, indent=2)

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        # Fast path has no position info
        token_list = [{"type": tt.name, "value": value} for tt, value in tokens]
        yield json.dumps(token_list, indent=2)

    def format_string(self, tokens, config=None):
        return "".join(self.format(tokens, config))

    def format_string_fast(self, tokens, config=None):
        return "".join(self.format_fast(tokens, config))


# Usage
from rosettes import highlight

output = highlight("x = 1", "python", formatter=JsonFormatter())
```

Output:

```json
[
  {"type": "NAME", "value": "x", "line": 1, "column": 1},
  {"type": "WHITESPACE", "value": " ", "line": 1, "column": 2},
  {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
  {"type": "WHITESPACE", "value": " ", "line": 1, "column": 4},
  {"type": "NUMBER_INTEGER", "value": "1", "line": 1, "column": 5}
]
```

## Using Custom Formatters

Pass custom formatter instances directly to `highlight()`:

```python
from rosettes import highlight

formatter = MarkdownFormatter()
output = highlight("def foo(): pass", "python", formatter=formatter)
```

## Token Type Reference

See [[docs/reference/token-types|Token Types]] for the complete list of token types to handle in your formatter.

## Next Steps

- [[docs/reference/api|API Reference]] — `tokenize()` function details
- [[docs/reference/token-types|Token Types]] — All available token types

