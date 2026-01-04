---
title: Raw Tokens
description: Access tokens directly for analysis, transformation, and metrics
draft: false
weight: 20
lang: en
type: doc
tags:
- tokens
- analysis
- customization
keywords:
- tokenize
- raw tokens
- analysis
- metrics
icon: data_object
---

# Raw Tokens

Access tokens directly for code analysis, transformation, or custom output.

## The `tokenize()` Function

The `tokenize()` function returns a list of `Token` objects without formatting:

```python
from rosettes import tokenize

tokens = tokenize("x = 1 + 2", "python")

for token in tokens:
    print(f"{token.type.name:20} {token.value!r:10} L{token.line}:C{token.column}")
```

Output:

```text
NAME                 'x'        L1:C1
WHITESPACE           ' '        L1:C2
OPERATOR             '='        L1:C3
WHITESPACE           ' '        L1:C4
NUMBER_INTEGER       '1'        L1:C5
WHITESPACE           ' '        L1:C6
OPERATOR             '+'        L1:C7
WHITESPACE           ' '        L1:C8
NUMBER_INTEGER       '2'        L1:C9
```

---

## Token Structure

Each `Token` is an immutable `NamedTuple`:

```python
from rosettes import Token, TokenType

token = Token(
    type=TokenType.KEYWORD,
    value="def",
    line=1,
    column=1,
)

# Access fields
token.type      # TokenType.KEYWORD
token.value     # "def"
token.line      # 1 (1-based)
token.column    # 1 (1-based)
```

Tokens are **immutable** and **thread-safe**.

---

## Use Cases

### Code Metrics

Count tokens by type:

```python
from collections import Counter
from rosettes import tokenize, TokenType

def count_token_types(code: str, language: str) -> Counter[TokenType]:
    tokens = tokenize(code, language)
    return Counter(token.type for token in tokens)

code = '''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
'''

counts = count_token_types(code, "python")
print(f"Keywords: {counts[TokenType.KEYWORD]}")
print(f"Functions: {counts[TokenType.NAME_FUNCTION]}")
print(f"Numbers: {counts[TokenType.NUMBER_INTEGER]}")
```

### Code Transformation

Strip comments from code:

```python
from rosettes import tokenize, TokenType

def strip_comments(code: str, language: str) -> str:
    tokens = tokenize(code, language)
    comment_types = {
        TokenType.COMMENT,
        TokenType.COMMENT_SINGLE,
        TokenType.COMMENT_MULTILINE,
    }
    return "".join(
        token.value for token in tokens
        if token.type not in comment_types
    )

code = '''
x = 1  # set x
y = 2  # set y
'''

print(strip_comments(code, "python"))
# x = 1  
# y = 2  
```

### Extract Identifiers

Find all function and variable names:

```python
from rosettes import tokenize, TokenType

def extract_names(code: str, language: str) -> dict[str, set[str]]:
    tokens = tokenize(code, language)
    
    functions = set()
    variables = set()
    
    for token in tokens:
        if token.type == TokenType.NAME_FUNCTION:
            functions.add(token.value)
        elif token.type == TokenType.NAME:
            variables.add(token.value)
    
    return {"functions": functions, "variables": variables}

code = "def greet(name): return f'Hello, {name}'"
names = extract_names(code, "python")

print(names)
# {'functions': {'greet'}, 'variables': {'name'}}
```

### Syntax Validation

Check for unbalanced brackets:

```python
from rosettes import tokenize, TokenType

def check_brackets(code: str, language: str) -> bool:
    tokens = tokenize(code, language)
    
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack = []
    
    for token in tokens:
        if token.type == TokenType.PUNCTUATION:
            if token.value in pairs:
                stack.append(token.value)
            elif token.value in pairs.values():
                if not stack:
                    return False
                if pairs[stack.pop()] != token.value:
                    return False
    
    return len(stack) == 0

print(check_brackets("def foo(): pass", "python"))  # True
print(check_brackets("foo(()", "python"))           # False
```

---

## Parallel Tokenization

For multiple code blocks, use `tokenize_many()`:

```python
from rosettes import tokenize_many

blocks = [
    ("def foo(): pass", "python"),
    ("const x = 1;", "javascript"),
    ("fn main() {}", "rust"),
]

results = tokenize_many(blocks)

for tokens in results:
    print(f"{len(tokens)} tokens")
```

On Python 3.14t (free-threaded), this provides true parallelism.

---

## Direct Lexer Access

For maximum control, use the lexer directly:

```python
from rosettes import get_lexer

lexer = get_lexer("python")

# Streaming tokenization (iterator)
for token in lexer.tokenize("x = 1"):
    print(token)

# Fast path (no position tracking)
for token_type, value in lexer.tokenize_fast("x = 1"):
    print(f"{token_type}: {value!r}")
```

The `tokenize_fast()` method returns `(TokenType, str)` tuples without line/column tracking—useful when you only need token types and values.

---

## Next Steps

- [[docs/reference/token-types|Token Types]] — Complete token type reference
- [[docs/extending/custom-formatter|Custom Formatter]] — Build custom output formats
- [[docs/reference/api|API Reference]] — Full API documentation

