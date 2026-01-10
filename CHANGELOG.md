# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-02

Initial public release of Rosettes, extracted from the Bengal static site generator.

### Added

- **Core API**
  - `highlight()` — Generate formatted output with syntax highlighting
  - `tokenize()` — Get raw tokens for custom processing
  - `highlight_many()` — Parallel highlighting for multiple blocks
  - `tokenize_many()` — Parallel tokenization

- **Formatter Registry**
  - `get_formatter()` — Get formatter by name or alias
  - `list_formatters()` — List all supported formatters
  - `supports_formatter()` — Check formatter support
  - Built-in formatters: HTML, Terminal, Null

- **Lexer Registry**
  - `get_lexer()` — Get lexer by name or alias
  - `list_languages()` — List all supported languages
  - `supports_language()` — Check language support

- **55 Language Lexers**
  - Hand-written state machines with O(n) guaranteed performance
  - Zero ReDoS vulnerabilities
  - Languages: Python, JavaScript, TypeScript, Rust, Go, C, C++, Java, Kotlin, Ruby, and 45 more

- **Styling Features**
  - Semantic CSS classes (`.syntax-keyword`, `.syntax-function`, etc.)
  - Pygments-compatible classes (`.k`, `.nf`, etc.)
  - Line highlighting with `hl_lines`
  - Line numbers with `show_linenos`

- **Python 3.14t Support**
  - Designed for free-threading (PEP 703)
  - Declared GIL-free safety via `_Py_mod_gil`
  - Thread-safe by design: lexers use only local variables

### Technical Details

- Pure Python — no runtime dependencies
- `py.typed` marker for type checking
- Comprehensive test suite

[0.1.0]: https://github.com/lbliii/rosettes/releases/tag/v0.1.0

