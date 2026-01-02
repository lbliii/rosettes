---
title: Custom Themes
description: Build your own syntax highlighting theme
draft: false
weight: 30
lang: en
type: doc
tags:
- themes
- css
keywords:
- custom theme
- colors
- styling
icon: palette
---

# Custom Themes

Create a custom syntax highlighting theme with semantic classes.

## Basic Theme Structure

```css
/* Container */
.rosettes {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 14px;
  line-height: 1.5;
}

.rosettes pre {
  margin: 0;
}

/* Keywords */
.syntax-keyword { color: #cba6f7; }
.syntax-keyword-constant { color: #fab387; }
.syntax-keyword-type { color: #89dceb; }

/* Names */
.syntax-function { color: #89b4fa; }
.syntax-class { color: #f9e2af; }
.syntax-decorator { color: #f5c2e7; }
.syntax-builtin { color: #fab387; }
.syntax-variable { color: #cdd6f4; }

/* Literals */
.syntax-string { color: #a6e3a1; }
.syntax-string-escape { color: #f5c2e7; }
.syntax-number { color: #fab387; }

/* Comments */
.syntax-comment { color: #6c7086; font-style: italic; }

/* Operators */
.syntax-operator { color: #89dceb; }
.syntax-punctuation { color: #bac2de; }
```

---

## Theme Variations

### Light Theme

```css
.rosettes.light,
.rosettes[data-theme="light"] {
  background: #eff1f5;
  color: #4c4f69;
}

.rosettes.light .syntax-keyword { color: #8839ef; }
.rosettes.light .syntax-function { color: #1e66f5; }
.rosettes.light .syntax-string { color: #40a02b; }
.rosettes.light .syntax-comment { color: #9ca0b0; }
```

### Auto Dark/Light

```css
/* Light mode (default) */
.rosettes {
  background: #eff1f5;
  color: #4c4f69;
}

.syntax-keyword { color: #8839ef; }

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .rosettes {
    background: #1e1e2e;
    color: #cdd6f4;
  }
  
  .syntax-keyword { color: #cba6f7; }
}
```

---

## Line Features

### Line Numbers

```css
.rosettes .lineno {
  color: #6c7086;
  user-select: none;
  padding-right: 1.5em;
  text-align: right;
  min-width: 2.5em;
  display: inline-block;
  border-right: 1px solid #313244;
  margin-right: 1em;
}
```

### Highlighted Lines

```css
.rosettes .hll {
  background: rgba(203, 166, 247, 0.1);
  display: block;
  margin: 0 -1em;
  padding: 0 1em;
  border-left: 3px solid #cba6f7;
}
```

---

## Language-Specific Styles

Use `data-language` for language-specific styling:

```css
/* Python-specific */
.rosettes[data-language="python"] .syntax-decorator {
  color: #f5c2e7;
  font-weight: bold;
}

/* Rust-specific */
.rosettes[data-language="rust"] .syntax-keyword-type {
  color: #fab387;
}

/* JSON keys */
.rosettes[data-language="json"] .syntax-attribute {
  color: #89b4fa;
}
```

---

## Complete Theme Example

Here's a complete "Catppuccin Mocha" inspired theme:

```css
/* Catppuccin Mocha for Rosettes */
.rosettes {
  --ctp-rosewater: #f5e0dc;
  --ctp-flamingo: #f2cdcd;
  --ctp-pink: #f5c2e7;
  --ctp-mauve: #cba6f7;
  --ctp-red: #f38ba8;
  --ctp-maroon: #eba0ac;
  --ctp-peach: #fab387;
  --ctp-yellow: #f9e2af;
  --ctp-green: #a6e3a1;
  --ctp-teal: #94e2d5;
  --ctp-sky: #89dceb;
  --ctp-sapphire: #74c7ec;
  --ctp-blue: #89b4fa;
  --ctp-lavender: #b4befe;
  --ctp-text: #cdd6f4;
  --ctp-subtext1: #bac2de;
  --ctp-subtext0: #a6adc8;
  --ctp-overlay2: #9399b2;
  --ctp-overlay1: #7f849c;
  --ctp-overlay0: #6c7086;
  --ctp-surface2: #585b70;
  --ctp-surface1: #45475a;
  --ctp-surface0: #313244;
  --ctp-base: #1e1e2e;
  --ctp-mantle: #181825;
  --ctp-crust: #11111b;
  
  background: var(--ctp-base);
  color: var(--ctp-text);
  padding: 1em;
  border-radius: 8px;
  overflow-x: auto;
}

.syntax-keyword { color: var(--ctp-mauve); }
.syntax-keyword-constant { color: var(--ctp-peach); }
.syntax-function { color: var(--ctp-blue); }
.syntax-class { color: var(--ctp-yellow); }
.syntax-string { color: var(--ctp-green); }
.syntax-number { color: var(--ctp-peach); }
.syntax-comment { color: var(--ctp-overlay0); font-style: italic; }
.syntax-operator { color: var(--ctp-sky); }
.syntax-decorator { color: var(--ctp-pink); }
.syntax-builtin { color: var(--ctp-red); }
```

---

## Next Steps

- [[docs/styling/css-classes|CSS Classes]] — Full class reference
- [[docs/reference/token-types|Token Types]] — Understand token categories

