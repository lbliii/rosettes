# ⌾⌾⌾ Rosettes

[![PyPI version](https://img.shields.io/pypi/v/rosettes.svg)](https://pypi.org/project/rosettes/)
[![Build Status](https://github.com/lbliii/rosettes/actions/workflows/tests.yml/badge.svg)](https://github.com/lbliii/rosettes/actions/workflows/tests.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://pypi.org/project/rosettes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Modern syntax highlighting for Python 3.14t**

```python
from rosettes import highlight

html = highlight("def hello(): print('world')", "python")
```

---

## Why Rosettes?

- **O(n) guaranteed** — Hand-written state machines, no regex backtracking
- **Zero ReDoS** — No exploitable patterns, safe for untrusted input
- **Thread-safe** — Immutable state, optimized for Python 3.14t free-threading
- **Pygments compatible** — Drop-in CSS class compatibility
- **55 languages** — Python, JavaScript, Rust, Go, and 51 more

---

## Installation

```bash
pip install rosettes
```

Requires Python 3.14+

---

## Quick Start

| Function | Description |
|----------|-------------|
| `highlight(code, lang)` | Generate HTML with syntax highlighting |
| `tokenize(code, lang)` | Get raw tokens for custom processing |
| `highlight_many(items)` | Parallel highlighting for multiple blocks |
| `list_languages()` | List all 55 supported languages |

---

## Features

| Feature | Description | Docs |
|---------|-------------|------|
| **Basic Highlighting** | `highlight()` and `tokenize()` functions | [Highlighting →](https://lbliii.github.io/rosettes/docs/highlighting/) |
| **Parallel Processing** | `highlight_many()` for multi-core systems | [Parallel →](https://lbliii.github.io/rosettes/docs/highlighting/parallel/) |
| **Line Highlighting** | Highlight specific lines, add line numbers | [Lines →](https://lbliii.github.io/rosettes/docs/highlighting/line-highlighting/) |
| **CSS Styling** | Semantic or Pygments-compatible classes | [Styling →](https://lbliii.github.io/rosettes/docs/styling/) |
| **Custom Formatters** | Build terminal, LaTeX, or custom output | [Extending →](https://lbliii.github.io/rosettes/docs/extending/) |

📚 **Full documentation**: [lbliii.github.io/rosettes](https://lbliii.github.io/rosettes/)

---

## Usage

<details>
<summary><strong>Basic Highlighting</strong> — Generate HTML from code</summary>

```python
from rosettes import highlight

# Basic highlighting
html = highlight("def foo(): pass", "python")
# <div class="rosettes" data-language="python">...</div>

# With line numbers
html = highlight(code, "python", show_linenos=True)

# Highlight specific lines
html = highlight(code, "python", hl_lines={2, 3, 4})
```

</details>

<details>
<summary><strong>Parallel Processing</strong> — Speed up multiple blocks</summary>

For 8+ code blocks, use `highlight_many()` for parallel processing:

```python
from rosettes import highlight_many

blocks = [
    ("def foo(): pass", "python"),
    ("const x = 1;", "javascript"),
    ("fn main() {}", "rust"),
]

# Highlight in parallel
results = highlight_many(blocks)
```

On Python 3.14t with free-threading, this provides 1.5-2x speedup for 50+ blocks.

</details>

<details>
<summary><strong>Tokenization</strong> — Raw tokens for custom processing</summary>

```python
from rosettes import tokenize

tokens = tokenize("x = 42", "python")
for token in tokens:
    print(f"{token.type.name}: {token.value!r}")
# NAME: 'x'
# WHITESPACE: ' '
# OPERATOR: '='
# WHITESPACE: ' '
# NUMBER_INTEGER: '42'
```

</details>

<details>
<summary><strong>CSS Class Styles</strong> — Semantic or Pygments</summary>

**Semantic (default)** — Readable, self-documenting:

```python
html = highlight(code, "python")
# <span class="syntax-keyword">def</span>
# <span class="syntax-function">hello</span>
```

```css
.syntax-keyword { color: #ff79c6; }
.syntax-function { color: #50fa7b; }
.syntax-string { color: #f1fa8c; }
```

**Pygments-compatible** — Use existing themes:

```python
html = highlight(code, "python", css_class_style="pygments")
# <span class="k">def</span>
# <span class="nf">hello</span>
```

</details>

---

## Supported Languages

<details>
<summary><strong>55 languages</strong> with full syntax support</summary>

| Category | Languages |
|----------|-----------|
| **Core** | Python, JavaScript, TypeScript, JSON, YAML, TOML, Bash, HTML, CSS, Diff |
| **Systems** | C, C++, Rust, Go, Zig |
| **JVM** | Java, Kotlin, Scala, Groovy, Clojure |
| **Apple** | Swift |
| **Scripting** | Ruby, Perl, PHP, Lua, R, PowerShell |
| **Functional** | Haskell, Elixir |
| **Data/Query** | SQL, CSV, GraphQL |
| **Markup** | Markdown, XML |
| **Config** | INI, Nginx, Dockerfile, Makefile, HCL |
| **Schema** | Protobuf |
| **Modern** | Dart, Julia, Nim, Gleam, V |
| **AI/ML** | Mojo, Triton, CUDA, Stan |
| **Other** | PKL, CUE, Tree, Kida, Jinja, Plaintext |

</details>

---

## Architecture

<details>
<summary><strong>State Machine Lexers</strong> — O(n) guaranteed</summary>

Every lexer is a hand-written finite state machine:

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

**Key properties:**
- Single character lookahead (O(n) guaranteed)
- No backtracking (no ReDoS possible)
- Immutable state (thread-safe)
- Local variables only (no shared mutable state)

</details>

<details>
<summary><strong>Thread Safety</strong> — Free-threading ready</summary>

All public APIs are thread-safe:
- Lexers use only local variables during tokenization
- Formatter state is immutable
- Registry uses `functools.cache` for memoization
- Module declares itself safe for free-threading (PEP 703)

</details>

---

## Performance

Benchmarked against Pygments on a 10,000-line Python file:

| Operation | Rosettes | Pygments | Speedup |
|-----------|----------|----------|---------|
| Tokenize | 12ms | 45ms | **3.75x** |
| Highlight | 18ms | 52ms | **2.89x** |
| Parallel (8 blocks) | 22ms | 48ms | **2.18x** |

---

## Documentation

📚 **[lbliii.github.io/rosettes](https://lbliii.github.io/rosettes/)**

| Section | Description |
|---------|-------------|
| [Get Started](https://lbliii.github.io/rosettes/docs/get-started/) | Installation and quickstart |
| [Highlighting](https://lbliii.github.io/rosettes/docs/highlighting/) | Core highlighting APIs |
| [Styling](https://lbliii.github.io/rosettes/docs/styling/) | CSS classes and themes |
| [Reference](https://lbliii.github.io/rosettes/docs/reference/) | Complete API documentation |
| [About](https://lbliii.github.io/rosettes/docs/about/) | Architecture and design |

---

## Development

```bash
git clone https://github.com/lbliii/rosettes.git
cd rosettes
uv sync --group dev
pytest
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
