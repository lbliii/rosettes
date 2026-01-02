---
title: Migrate from Pygments
description: Switch from Pygments to Rosettes for HTML highlighting
draft: false
weight: 10
lang: en
type: doc
tags:
- migration
- pygments
keywords:
- migration
- pygments
- switch
icon: arrow-right
---

# Migrate from Pygments

Switch from Pygments to Rosettes for faster, safer HTML syntax highlighting.

## Prerequisites

- Python 3.14+
- Existing Pygments-based highlighting
- HTML output (Rosettes doesn't support LaTeX, RTF, etc.)

## Step 1: Install Rosettes

```bash
pip install rosettes
```

## Step 2: Update Imports

**Before (Pygments):**

```python
from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter
```

**After (Rosettes):**

```python
from rosettes import highlight, supports_language
```

## Step 3: Update Highlighting Calls

**Before (Pygments):**

```python
def highlight_code(code: str, language: str) -> str:
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        lexer = TextLexer()
    
    formatter = HtmlFormatter(cssclass="highlight")
    return highlight(code, lexer, formatter)
```

**After (Rosettes):**

```python
def highlight_code(code: str, language: str) -> str:
    if not supports_language(language):
        language = "plaintext"
    
    return highlight(code, language, css_class_style="pygments")
```

Key differences:
- Single import instead of three
- `css_class_style="pygments"` for theme compatibility
- `supports_language()` for validation

## Step 4: Keep Your CSS

Your existing Pygments CSS theme works unchanged:

```css
/* Your existing Pygments theme */
.highlight { background: #272822; }
.highlight .k { color: #66d9ef; }
.highlight .nf { color: #a6e22e; }
/* ... */
```

Rosettes generates the same CSS classes when using `css_class_style="pygments"`.

## Step 5: Update Line Highlighting (Optional)

**Before (Pygments):**

```python
formatter = HtmlFormatter(
    linenos=True,
    hl_lines=[2, 3, 4],
)
```

**After (Rosettes):**

```python
html = highlight(
    code,
    language,
    show_linenos=True,
    hl_lines={2, 3, 4},  # Note: set, not list
    css_class_style="pygments",
)
```

## Step 6: Update Parallel Highlighting (Optional)

**Before (Pygments):**

```python
from concurrent.futures import ThreadPoolExecutor

def highlight_many_pygments(blocks):
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(
            lambda b: highlight_code(b[0], b[1]),
            blocks
        ))
```

**After (Rosettes):**

```python
from rosettes import highlight_many

def highlight_many_rosettes(blocks):
    return highlight_many(blocks, css_class_style="pygments")
```

Built-in, optimized, and thread-safe.

## Complete Migration Example

**Before:**

```python
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.lexers import ClassNotFound
from pygments.formatters import HtmlFormatter

class CodeHighlighter:
    def __init__(self):
        self.formatter = HtmlFormatter(cssclass="highlight")
    
    def highlight(self, code: str, language: str) -> str:
        try:
            lexer = get_lexer_by_name(language)
        except ClassNotFound:
            lexer = TextLexer()
        return highlight(code, lexer, self.formatter)
    
    def highlight_with_lines(
        self,
        code: str,
        language: str,
        hl_lines: list[int],
    ) -> str:
        try:
            lexer = get_lexer_by_name(language)
        except ClassNotFound:
            lexer = TextLexer()
        formatter = HtmlFormatter(
            cssclass="highlight",
            linenos=True,
            hl_lines=hl_lines,
        )
        return highlight(code, lexer, formatter)
```

**After:**

```python
from rosettes import highlight, highlight_many, supports_language

class CodeHighlighter:
    def highlight(self, code: str, language: str) -> str:
        if not supports_language(language):
            language = "plaintext"
        return highlight(code, language, css_class_style="pygments")
    
    def highlight_with_lines(
        self,
        code: str,
        language: str,
        hl_lines: set[int],
    ) -> str:
        if not supports_language(language):
            language = "plaintext"
        return highlight(
            code,
            language,
            show_linenos=True,
            hl_lines=hl_lines,
            css_class_style="pygments",
        )
    
    def highlight_batch(
        self,
        blocks: list[tuple[str, str]],
    ) -> list[str]:
        # Validate languages
        validated = [
            (code, lang if supports_language(lang) else "plaintext")
            for code, lang in blocks
        ]
        return highlight_many(validated, css_class_style="pygments")
```

## API Mapping

| Pygments | Rosettes |
|----------|----------|
| `get_lexer_by_name(lang)` | `get_lexer(lang)` |
| `ClassNotFound` exception | `LookupError` exception |
| `supports_language()` check | `supports_language(lang)` |
| `HtmlFormatter(cssclass=...)` | `highlight(..., css_class=...)` |
| `HtmlFormatter(linenos=True)` | `highlight(..., show_linenos=True)` |
| `hl_lines=[1,2,3]` | `hl_lines={1,2,3}` (set) |

## Known Differences

| Aspect | Pygments | Rosettes |
|--------|----------|----------|
| Languages | 500+ | 55 |
| Output formats | HTML, LaTeX, RTF, etc. | HTML only |
| `hl_lines` type | `list` | `set` or `frozenset` |
| Line number format | Configurable | Fixed format |

## Verification

After migration, verify:

1. **Output looks the same**: Compare rendered HTML
2. **CSS classes match**: Inspect generated class names
3. **Performance improved**: Benchmark before/after
4. **No errors**: Test with all your languages

```python
# Quick verification
from rosettes import highlight

html = highlight("def foo(): pass", "python", css_class_style="pygments")
assert '<span class="k">def</span>' in html
assert '<span class="nf">foo</span>' in html
print("✅ Migration successful!")
```

## Next Steps

- [[docs/highlighting/parallel|Parallel Processing]] — Optimize batch highlighting
- [[docs/about/comparison|Comparison]] — Full Rosettes vs Pygments comparison
- [[docs/styling/pygments-themes|Pygments Themes]] — Theme compatibility details

