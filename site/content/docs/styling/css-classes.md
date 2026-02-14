---
title: CSS Classes
description: Complete reference for semantic and Pygments CSS classes
draft: false
weight: 10
lang: en
type: doc
tags:
- css
- classes
keywords:
- css classes
- semantic
- syntax highlighting
icon: tag
---

# CSS Classes

Rosettes outputs two class styles: semantic (readable) and Pygments (compatible).

## Semantic Classes

Semantic mode uses role-based class names. Each token maps to a `SyntaxRole`, which determines the CSS class. Themes define colors for roles, not individual token types.

### Control & Structure

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-control` | CONTROL_FLOW | `if`, `for`, `while`, `return`, `and`, `or` |
| `.syntax-declaration` | DECLARATION | `def`, `class`, `let`, `const`, `var` |
| `.syntax-import` | IMPORT | `import`, `from`, `as`, `#include` |

### Data & Literals

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-string` | STRING | `"hello"`, `'world'`, `` `backtick` `` |
| `.syntax-docstring` | DOCSTRING | `"""docstring"""`, `/** comment */` |
| `.syntax-number` | NUMBER | `42`, `3.14`, `0xff`, `0b1010` |
| `.syntax-boolean` | BOOLEAN | `True`, `False`, `None` |

### Identifiers

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-type` | TYPE | `MyClass`, `int`, `str`, `ValueError` |
| `.syntax-function` | FUNCTION | `foo`, `print`, `len`, `range` |
| `.syntax-variable` | VARIABLE | `my_var`, `x`, `count` |
| `.syntax-constant` | CONSTANT | `PI`, `MAX_SIZE`, `self`, `__name__` |
| `.syntax-attribute` | ATTRIBUTE | `@property`, `.name`, `.value` |
| `.syntax-namespace` | NAMESPACE | `package.module`, `std.io` |
| `.syntax-tag` | TAG | HTML/XML tag names |

### Documentation

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-comment` | COMMENT | `# comment`, `// comment`, `/* ... */` |
| `.syntax-docstring` | DOCSTRING | `"""docstring"""` |

### Operators & Punctuation

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-operator` | OPERATOR | `+`, `-`, `=`, `*`, `/` |
| `.syntax-punctuation` | PUNCTUATION | `(`, `)`, `,`, `;`, `:` |

### Special

| Class | Role | Example Tokens |
|-------|------|----------------|
| `.syntax-string` | STRING (escape) | `\n`, `\t` in strings |
| `.syntax-regex` | REGEX | `/pattern/` in JavaScript |
| `.syntax-error` | ERROR | Invalid syntax tokens |
| `.syntax-warning` | WARNING | Diagnostic markers |
| `.syntax-added` | ADDED | `+added` in diffs |
| `.syntax-removed` | REMOVED | `-removed` in diffs |
| `.syntax-muted` | MUTED | Less prominent elements |

Note: Plain text and whitespace receive no span (no class). They use the default text color.

---

## Pygments Classes

For drop-in compatibility with Pygments themes, use `css_class_style="pygments"`. Token types map directly to Pygments CSS class suffixes.

### Keywords

| Pygments | Semantic Role | Description |
|----------|---------------|-------------|
| `.k` | `.syntax-control` | Keyword |
| `.kc` | `.syntax-boolean` | Keyword.Constant |
| `.kd` | `.syntax-declaration` | Keyword.Declaration |
| `.kn` | `.syntax-import` | Keyword.Namespace |
| `.kt` | `.syntax-type` | Keyword.Type |

### Names

| Pygments | Semantic Role | Description |
|----------|---------------|-------------|
| `.n` | `.syntax-variable` | Name |
| `.nf` | `.syntax-function` | Name.Function |
| `.nc` | `.syntax-type` | Name.Class |
| `.nd` | `.syntax-attribute` | Name.Decorator |
| `.nb` | `.syntax-function` | Name.Builtin |
| `.nv` | `.syntax-variable` | Name.Variable |
| `.na` | `.syntax-attribute` | Name.Attribute |

### Literals

| Pygments | Semantic Role | Description |
|----------|---------------|-------------|
| `.s` | `.syntax-string` | String |
| `.se` | `.syntax-escape` | String.Escape |
| `.si` | `.syntax-escape` | String.Interpol |
| `.m` | `.syntax-number` | Number |
| `.mf` | `.syntax-number` | Number.Float |
| `.mh` | `.syntax-number` | Number.Hex |

### Comments

| Pygments | Semantic Role | Description |
|----------|---------------|-------------|
| `.c` | `.syntax-comment` | Comment |
| `.c1` | `.syntax-comment` | Comment.Single |
| `.cm` | `.syntax-comment` | Comment.Multiline |
| `.sd` | `.syntax-docstring` | String.Doc |

### Operators & Punctuation

| Pygments | Semantic Role | Description |
|----------|---------------|-------------|
| `.o` | `.syntax-operator` | Operator |
| `.p` | `.syntax-punctuation` | Punctuation |

---

## Hybrid Mode

Use `css_class_style="semantic-hybrid"` to emit both role and token-type classes. This lets themes distinguish e.g. builtins from user-defined functions:

```python
>>> from rosettes import highlight
>>> html = highlight("print(x)", "python", css_class_style="semantic-hybrid")
>>> "syntax-function" in html and "syntax-name-builtin" in html
True
```

Output: `class="syntax-function syntax-name-builtin"` for `print`, `class="syntax-variable syntax-name"` for `x`.

Override in CSS:

```css
.syntax-name-builtin { color: var(--syntax-builtin); }
.syntax-function { color: var(--syntax-function); }
```

---

## Container Classes

The HTML output is wrapped in a container:

```html
<div class="rosettes" data-language="python">
  <pre><code>...</code></pre>
</div>
```

| Class | Description |
|-------|-------------|
| `.rosettes` | Container (semantic style) |
| `.highlight` | Container (pygments style) |
| `.lineno` | Line number |
| `.line` | Line wrapper |
| `.hll` | Highlighted line |

---

## Next Steps

- [[docs/styling/pygments-themes|Pygments Themes]] — Use existing Pygments themes
- [[docs/styling/custom-themes|Custom Themes]] — Build your own theme
