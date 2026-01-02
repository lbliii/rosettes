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

Formatters implement a simple protocol:

```python
from typing import Protocol, Iterable
from rosettes import Token, FormatConfig

class Formatter(Protocol):
    def format_string(
        self,
        tokens: Iterable[Token],
        config: FormatConfig,
    ) -> str: ...
```

## Example: Terminal Formatter

A formatter that outputs ANSI-colored terminal text:

```python
from rosettes import tokenize, Token, TokenType, FormatConfig

# ANSI color codes
COLORS = {
    TokenType.KEYWORD: "\033[95m",      # Magenta
    TokenType.NAME_FUNCTION: "\033[92m", # Green
    TokenType.STRING: "\033[93m",        # Yellow
    TokenType.COMMENT: "\033[90m",       # Gray
    TokenType.NUMBER: "\033[94m",        # Blue
}
RESET = "\033[0m"

class TerminalFormatter:
    def format_string(
        self,
        tokens: Iterable[Token],
        config: FormatConfig,
    ) -> str:
        result = []
        for token in tokens:
            color = COLORS.get(token.type, "")
            if color:
                result.append(f"{color}{token.value}{RESET}")
            else:
                result.append(token.value)
        return "".join(result)

# Usage
tokens = tokenize("def hello(): print('world')", "python")
formatter = TerminalFormatter()
output = formatter.format_string(tokens, FormatConfig())
print(output)  # Colored terminal output
```

## Example: Markdown Formatter

A formatter that outputs fenced code blocks:

```python
class MarkdownFormatter:
    def format_string(
        self,
        tokens: Iterable[Token],
        config: FormatConfig,
    ) -> str:
        code = "".join(token.value for token in tokens)
        lang = config.data_language or ""
        return f"```{lang}\n{code}\n```"

# Usage
tokens = tokenize("x = 1", "python")
formatter = MarkdownFormatter()
output = formatter.format_string(tokens, FormatConfig(data_language="python"))
# ```python
# x = 1
# ```
```

## Example: JSON Token Dump

Export tokens as JSON for analysis:

```python
import json
from rosettes import tokenize, FormatConfig

class JsonFormatter:
    def format_string(
        self,
        tokens: Iterable[Token],
        config: FormatConfig,
    ) -> str:
        token_list = [
            {
                "type": token.type.name,
                "value": token.value,
                "line": token.line,
                "column": token.column,
            }
            for token in tokens
        ]
        return json.dumps(token_list, indent=2)

# Usage
tokens = tokenize("x = 1", "python")
formatter = JsonFormatter()
print(formatter.format_string(tokens, FormatConfig()))
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

Custom formatters work with `tokenize()`:

```python
from rosettes import tokenize, FormatConfig

def highlight_custom(code: str, language: str, formatter) -> str:
    tokens = tokenize(code, language)
    config = FormatConfig(data_language=language)
    return formatter.format_string(tokens, config)

# Usage
output = highlight_custom("def foo(): pass", "python", TerminalFormatter())
```

## Token Type Reference

See [[docs/reference/token-types|Token Types]] for the complete list of token types to handle in your formatter.

## Next Steps

- [[docs/reference/api|API Reference]] — `tokenize()` function details
- [[docs/reference/token-types|Token Types]] — All available token types

