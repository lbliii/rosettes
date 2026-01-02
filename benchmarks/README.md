# Rosettes Benchmarks

Benchmarks comparing Rosettes vs Pygments performance.

## Quick Start

```bash
# Install benchmark dependencies
pip install pygments pytest-benchmark

# Run CLI benchmark (no pytest-benchmark required)
python -m benchmarks.benchmark_vs_pygments

# Run with pytest-benchmark for detailed stats
pytest benchmarks/ -v --benchmark-only
```

## What's Tested

| Category | Description |
|----------|-------------|
| **Single file** | Python, Rust, JavaScript, Go at various sizes |
| **Parallel** | `highlight_many()` vs sequential Pygments |
| **Large files** | 10,000 line Python file |

## Expected Results

On typical hardware, Rosettes shows:

- **2-4x faster** on medium files (~50 lines)
- **3-5x faster** on large files (~500+ lines)
- **Additional gains** with `highlight_many()` on Python 3.14t (free-threaded)

## Files

- `benchmark_vs_pygments.py` - Main Rosettes vs Pygments comparison
- `sample_code.py` - Code samples used in benchmarks
- `conftest.py` - pytest configuration

## Running Specific Tests

```bash
# Only Rosettes tests
pytest benchmarks/ -v --benchmark-only -k "rosettes"

# Only large file tests
pytest benchmarks/ -v --benchmark-only -m slow

# Skip slow tests
pytest benchmarks/ -v --benchmark-only -m "not slow"
```

## Interpreting Results

The key metrics are:

- **Mean time**: Average execution time (use for comparisons)
- **Speedup**: Pygments time / Rosettes time

Lower is better for times. Higher is better for speedup.

