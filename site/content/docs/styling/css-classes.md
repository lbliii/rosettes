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

Self-documenting class names that describe what the token represents.

### Keywords

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-keyword` | Language keywords | `def`, `class`, `if` |
| `.syntax-keyword-constant` | Constant keywords | `True`, `False`, `None` |
| `.syntax-keyword-declaration` | Declaration keywords | `let`, `const`, `var` |
| `.syntax-keyword-namespace` | Namespace keywords | `import`, `from`, `as` |
| `.syntax-keyword-type` | Type keywords | `int`, `str`, `bool` |

### Names

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-function` | Function names | `print`, `len` |
| `.syntax-class` | Class names | `MyClass` |
| `.syntax-decorator` | Decorators | `@property` |
| `.syntax-builtin` | Built-in names | `print`, `len`, `range` |
| `.syntax-variable` | Variable names | `my_var` |
| `.syntax-attribute` | Attributes | `.name`, `.value` |

### Literals

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-string` | String literals | `"hello"`, `'world'` |
| `.syntax-string-escape` | Escape sequences | `\n`, `\t` |
| `.syntax-string-interpol` | Interpolation | `{name}` in f-strings |
| `.syntax-number` | All numbers | `42`, `3.14`, `0xff` |
| `.syntax-number-float` | Float numbers | `3.14` |
| `.syntax-number-hex` | Hex numbers | `0xff` |

### Comments

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-comment` | All comments | `# comment` |
| `.syntax-comment-single` | Single-line | `# comment` |
| `.syntax-comment-multiline` | Multi-line | `/* ... */` |
| `.syntax-comment-doc` | Doc comments | `"""docstring"""` |

### Operators & Punctuation

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-operator` | Operators | `+`, `-`, `=` |
| `.syntax-punctuation` | Punctuation | `(`, `)`, `,` |

### Special

| Class | Description | Example |
|-------|-------------|---------|
| `.syntax-text` | Plain text | Unclassified text |
| `.syntax-whitespace` | Whitespace | Spaces, tabs |
| `.syntax-error` | Error tokens | Invalid syntax |

---

## Pygments Classes

For drop-in compatibility with Pygments themes.

### Keywords

| Pygments | Semantic Equivalent | Description |
|----------|---------------------|-------------|
| `.k` | `.syntax-keyword` | Keyword |
| `.kc` | `.syntax-keyword-constant` | Keyword.Constant |
| `.kd` | `.syntax-keyword-declaration` | Keyword.Declaration |
| `.kn` | `.syntax-keyword-namespace` | Keyword.Namespace |
| `.kt` | `.syntax-keyword-type` | Keyword.Type |

### Names

| Pygments | Semantic Equivalent | Description |
|----------|---------------------|-------------|
| `.n` | `.syntax-name` | Name |
| `.nf` | `.syntax-function` | Name.Function |
| `.nc` | `.syntax-class` | Name.Class |
| `.nd` | `.syntax-decorator` | Name.Decorator |
| `.nb` | `.syntax-builtin` | Name.Builtin |
| `.nv` | `.syntax-variable` | Name.Variable |
| `.na` | `.syntax-attribute` | Name.Attribute |

### Literals

| Pygments | Semantic Equivalent | Description |
|----------|---------------------|-------------|
| `.s` | `.syntax-string` | String |
| `.se` | `.syntax-string-escape` | String.Escape |
| `.si` | `.syntax-string-interpol` | String.Interpol |
| `.m` | `.syntax-number` | Number |
| `.mf` | `.syntax-number-float` | Number.Float |
| `.mh` | `.syntax-number-hex` | Number.Hex |

### Comments

| Pygments | Semantic Equivalent | Description |
|----------|---------------------|-------------|
| `.c` | `.syntax-comment` | Comment |
| `.c1` | `.syntax-comment-single` | Comment.Single |
| `.cm` | `.syntax-comment-multiline` | Comment.Multiline |
| `.sd` | `.syntax-comment-doc` | String.Doc |

### Operators & Punctuation

| Pygments | Semantic Equivalent | Description |
|----------|---------------------|-------------|
| `.o` | `.syntax-operator` | Operator |
| `.p` | `.syntax-punctuation` | Punctuation |

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

