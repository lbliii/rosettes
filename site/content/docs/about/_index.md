---
title: About
description: Architecture, comparisons, and design philosophy for the Rosettes Python syntax highlighter
draft: false
weight: 00
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
- python syntax highlighter
- pygments alternative
icon: info
---

# About Rosettes

Rosettes is a modern syntax highlighter designed for Python 3.14's free-threading era.
This section explains why it fits teams that care about safe highlighting,
predictable performance, and Pygments-compatible output.

## Core Principles

| Principle | Meaning |
|-----------|---------|
| **O(n) guaranteed** | Linear time complexity, no exponential blowup |
| **Zero ReDoS** | No regex patterns that can be exploited |
| **Thread-safe by design** | Immutable state, no global mutable data |
| **Pygments compatible** | Drop-in CSS class compatibility |

## Why Rosettes?

Traditional syntax highlighters use regular expressions, which can exhibit exponential worst-case behavior (ReDoS). A carefully crafted input can freeze your application for minutes or hours.

Rosettes eliminates this risk entirely by using hand-written state machine lexers. Every lexer processes input character-by-character with no backtracking, guaranteeing O(n) time complexity.

## In This Section

:::{child-cards}
:columns: 2
:include: pages
:fields: title, description, icon
:::

