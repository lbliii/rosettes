---
title: Get Started
description: Install Rosettes and highlight your first code block
draft: false
weight: 10
lang: en
type: doc
tags:
- onboarding
- quickstart
keywords:
- getting started
- installation
- quickstart
category: onboarding
cascade:
  type: doc
icon: arrow-clockwise
---

# Get Started

## Install

```bash
pip install rosettes
```

Requires Python 3.14 or later. See [[docs/get-started/installation|installation]] for alternative methods.

## Highlight Code

```python
from rosettes import highlight

html = highlight("def hello(): print('world')", "python")
print(html)
```

Output:

```html
<div class="rosettes" data-language="python">
  <pre><code><span class="syntax-keyword">def</span> ...
```

## What's Next?

:::{cards}
:columns: 1-2-3
:gap: medium

:::{card} Quickstart
:icon: zap
:link: ./quickstart
:description: Highlight code in 2 minutes
:badge: Start Here
Complete walkthrough from install to styled output.
:::{/card}

:::{card} Parallel Processing
:icon: cpu
:link: ../highlighting/parallel
:description: Process multiple blocks concurrently
For sites with many code blocks, `highlight_many()` provides 1.5-2x speedup.
:::{/card}

:::{card} Styling
:icon: palette
:link: ../styling/
:description: CSS classes and themes
Use semantic classes or Pygments-compatible themes.
:::{/card}

:::{/cards}

## Quick Links

- [[docs/reference/api|API Reference]] — Complete function signatures
- [[docs/reference/languages|Languages]] — All 55 supported languages
- [[docs/about/comparison|vs Pygments]] — Feature and performance comparison

