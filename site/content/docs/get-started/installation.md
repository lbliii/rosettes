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

:::{checklist} Prerequisites
:show-progress:
- [ ] Python 3.14+ installed
- [x] No runtime dependencies (pure Python)
:::{/checklist}

## Install

:::{tab-set}
:::{tab-item} uv

```bash
uv add rosettes
```

:::{/tab-item}

:::{tab-item} pip

```bash
pip install rosettes
```

:::{/tab-item}

:::{tab-item} From Source

```bash
git clone https://github.com/lbliii/rosettes.git
cd rosettes
pip install -e .
```

:::{/tab-item}
:::{/tab-set}

## Verify Installation

```python
import rosettes
print(rosettes.__version__)  # 0.1.0
```

Or from the command line:

```bash
python -c "import rosettes; print(rosettes.__version__)"
```

## Python 3.14t (Free-Threading)

Rosettes is optimized for Python 3.14t with free-threading enabled (PEP 703). To use free-threading:

:::{steps}
:::{step} Build or install Python 3.14 with `--disable-gil`

Use the free-threaded build (e.g. `python3.14t`).

:::{/step}
:::{step} Install Rosettes normally

Use pip or uv as shown above.

:::{/step}
:::{step} Use highlight_many() for true parallelism

For batch highlighting with true parallelism.

:::{/step}
:::{/steps}

```python
from rosettes import highlight_many

# On 3.14t, this runs with true parallelism
blocks = [("code", "python") for _ in range(100)]
results = highlight_many(blocks)  # 1.5-2x speedup
```

See [[docs/about/thread-safety|Thread Safety]] for details on Rosettes' free-threading support.

## Next Steps

:::{related}
:limit: 3
:section_title: Next Steps
:::

