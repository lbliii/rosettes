---
title: About
description: Architecture, design philosophy, and background
draft: false
weight: 60
lang: en
type: doc
cascade:
  type: doc
tags:
- about
- architecture
keywords:
- about
- architecture
- philosophy
icon: info
---

# About Rosettes

Rosettes is a modern syntax highlighter designed for Python 3.14's free-threading era. Every design decision prioritizes safety, predictability, and performance.

## Core Principles

| Principle | Meaning |
|-----------|---------|
| **O(n) guaranteed** | Linear time complexity, no exponential blowup |
| **Zero ReDoS** | No regex patterns that can be exploited |
| **Thread-safe by design** | Immutable state, no global mutable data |
| **Pygments compatible** | Drop-in CSS class compatibility |

## Why Rosettes?

Traditional syntax highlighters use regular expressions, which can exhibit exponential worst-case behavior (ReDoS). A carefully crafted input can freeze your application for minutes or hours.

Rosettes eliminates this risk entirely by using hand-written state machine lexers. Every lexer processes input character-by-character with single-character lookahead, guaranteeing O(n) time complexity.

## In This Section

:::{child-cards}
:columns: 2
:include: pages
:fields: title, description, icon
:::

