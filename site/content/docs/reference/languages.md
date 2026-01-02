---
title: Supported Languages
description: All 55 supported languages with aliases
draft: false
weight: 30
lang: en
type: doc
tags:
- languages
- reference
keywords:
- languages
- supported
- lexers
icon: globe
---

# Supported Languages

Rosettes supports 55 languages with hand-written state machine lexers.

## Language List

### Core Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `python` | `py`, `python3` | Python 3.x |
| `javascript` | `js` | JavaScript/ECMAScript |
| `typescript` | `ts` | TypeScript |
| `json` | | JSON data format |
| `yaml` | `yml` | YAML configuration |
| `toml` | | TOML configuration |
| `bash` | `sh`, `shell`, `zsh` | Bash/shell scripts |
| `html` | | HTML markup |
| `css` | | CSS stylesheets |
| `diff` | `patch` | Unified diff format |

### Systems Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `c` | | C programming language |
| `cpp` | `c++`, `cxx` | C++ programming language |
| `rust` | `rs` | Rust programming language |
| `go` | `golang` | Go programming language |
| `zig` | | Zig programming language |

### JVM Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `java` | | Java programming language |
| `kotlin` | `kt` | Kotlin programming language |
| `scala` | | Scala programming language |
| `groovy` | | Groovy programming language |
| `clojure` | `clj` | Clojure programming language |

### Apple Ecosystem

| Language | Aliases | Description |
|----------|---------|-------------|
| `swift` | | Swift programming language |

### Scripting Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `ruby` | `rb` | Ruby programming language |
| `perl` | `pl` | Perl programming language |
| `php` | | PHP programming language |
| `lua` | | Lua programming language |
| `r` | | R statistical language |
| `powershell` | `ps1`, `pwsh` | PowerShell scripting |

### Functional Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `haskell` | `hs` | Haskell programming language |
| `elixir` | `ex`, `exs` | Elixir programming language |

### Data & Query Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `sql` | | SQL query language |
| `csv` | | CSV data format |
| `graphql` | `gql` | GraphQL query language |

### Markup Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `markdown` | `md` | Markdown markup |
| `xml` | | XML markup |

### Configuration Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `ini` | `cfg`, `conf` | INI configuration |
| `nginx` | | Nginx configuration |
| `dockerfile` | `docker` | Dockerfile |
| `makefile` | `make` | Makefile |
| `hcl` | `terraform`, `tf` | HashiCorp Configuration Language |

### Schema Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `protobuf` | `proto` | Protocol Buffers |

### Modern Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `dart` | | Dart programming language |
| `julia` | `jl` | Julia programming language |
| `nim` | | Nim programming language |
| `gleam` | | Gleam programming language |
| `v` | `vlang` | V programming language |

### AI/ML Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `mojo` | `🔥` | Mojo programming language |
| `triton` | | Triton GPU language |
| `cuda` | `cu` | CUDA C/C++ |
| `stan` | | Stan probabilistic language |

### Other Languages

| Language | Aliases | Description |
|----------|---------|-------------|
| `pkl` | | Apple Pkl configuration |
| `cue` | | CUE configuration |
| `tree` | | Tree-sitter output |
| `kida` | | Kida template language |
| `jinja` | `jinja2`, `j2` | Jinja2 templates |
| `plaintext` | `text`, `txt` | Plain text (no highlighting) |

---

## Checking Language Support

```python
from rosettes import list_languages, supports_language

# List all languages
print(list_languages())
# ['bash', 'c', 'clojure', 'cpp', 'css', ...]

# Check specific language
supports_language("python")   # True
supports_language("py")       # True (alias)
supports_language("cobol")    # False
```

---

## Using Aliases

All aliases map to their canonical language:

```python
from rosettes import highlight

# These are all equivalent
highlight(code, "python")
highlight(code, "py")
highlight(code, "python3")

# JavaScript aliases
highlight(code, "javascript")
highlight(code, "js")

# Bash aliases
highlight(code, "bash")
highlight(code, "sh")
highlight(code, "shell")
```

---

## Language Detection

Rosettes does not include automatic language detection. Specify the language explicitly:

```python
# Always specify the language
html = highlight(code, "python")
```

For automatic detection, consider using a separate library like `pygments.lexers.guess_lexer()` or filename-based detection.

