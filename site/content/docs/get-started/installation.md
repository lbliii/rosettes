---
title: Installation
description: Install Rosettes using pip, uv, or from source
draft: false
weight: 10
lang: en
type: doc
tags:
- installation
keywords:
- install
- pip
- uv
- python 3.14
icon: download
---

# Installation

## Requirements

- **Python 3.14+** (required)
- No runtime dependencies (pure Python)

## Using pip

```bash
pip install rosettes
```

## Using uv

```bash
uv add rosettes
```

## From Source

```bash
git clone https://github.com/lbliii/rosettes.git
cd rosettes
pip install -e .
```

## Verify Installation

```python
import rosettes
print(rosettes.__version__)  # 0.3.0
```

Or from the command line:

```bash
python -c "import rosettes; print(rosettes.__version__)"
```

## Python 3.14t (Free-Threading)

Rosettes is optimized for Python 3.14t with free-threading enabled (PEP 703). To use free-threading:

1. Build or install Python 3.14 with `--disable-gil`
2. Install Rosettes normally
3. Use `highlight_many()` for true parallelism

```python
from rosettes import highlight_many

# On 3.14t, this runs with true parallelism
blocks = [("code", "python") for _ in range(100)]
results = highlight_many(blocks)  # 1.5-2x speedup
```

See [[docs/about/thread-safety|Thread Safety]] for details on Rosettes' free-threading support.

