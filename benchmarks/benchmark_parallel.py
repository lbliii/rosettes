"""Parallel highlighting benchmark for free-threading visibility.

Run with:
    python benchmarks/benchmark_parallel.py
    python -m benchmarks.benchmark_parallel

Demonstrates thread scaling when highlighting many code blocks in parallel
under Python 3.14t free-threading. Uses highlight_many() for parallel path
and sequential highlight() loop for baseline. Stdlib only.
"""

import sys
import time
from pathlib import Path


def _load_sample_code() -> None:
    """Add repo root to path and load sample_code (for script execution)."""
    _repo_root = Path(__file__).resolve().parent.parent
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))


def make_blocks(n: int) -> list[tuple[str, str]]:
    """Create n code blocks with varied languages (Python, JS, Rust, Go)."""
    _load_sample_code()
    from benchmarks.sample_code import (
        GO_CODE,
        JAVASCRIPT_CODE,
        PYTHON_MEDIUM,
        PYTHON_SIMPLE,
        RUST_CODE,
    )

    templates = [
        (PYTHON_SIMPLE, "python"),
        (PYTHON_MEDIUM, "python"),
        (RUST_CODE, "rust"),
        (JAVASCRIPT_CODE, "javascript"),
        (GO_CODE, "go"),
    ]
    return [templates[i % len(templates)] for i in range(n)]


def run_sequential(blocks: list[tuple[str, str]], iterations: int = 5) -> float:
    """Highlight blocks sequentially with highlight()."""
    from rosettes import highlight

    times: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        for code, lang in blocks:
            highlight(code, lang)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


def run_parallel(blocks: list[tuple[str, str]], max_workers: int, iterations: int = 5) -> float:
    """Highlight blocks in parallel with highlight_many()."""
    from rosettes import highlight_many

    times: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        highlight_many(blocks, max_workers=max_workers)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


def main() -> None:
    """Run parallel highlighting benchmark and print results."""
    # GIL detection
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    if gil_enabled:
        print("Free-threaded build: No (GIL enabled)")
        print("\nRun with Python 3.14t (free-threading) to see parallel scaling.")
        print("Example: python3.14t benchmarks/benchmark_parallel.py")
    else:
        version = sys.version.split()[0]
        print(f"Free-threaded build: Yes ({version})")

    n_blocks = 100
    blocks = make_blocks(n_blocks)
    print(f"\nParallel highlighting benchmark: {n_blocks} code blocks\n")

    # Warmup
    from rosettes import highlight

    for code, lang in blocks[:5]:
        highlight(code, lang)

    # Benchmark: 1 thread = sequential, 2/4/8 = highlight_many with max_workers
    results: list[tuple[int, float, float]] = []
    baseline_time: float | None = None

    for num_threads in [1, 2, 4, 8]:
        if num_threads == 1:
            elapsed = run_sequential(blocks)
        else:
            elapsed = run_parallel(blocks, max_workers=num_threads)
        if baseline_time is None:
            baseline_time = elapsed
        speedup = baseline_time / elapsed
        results.append((num_threads, elapsed, speedup))

    # Print table
    print("  Threads    Time      Speedup")
    for num_threads, elapsed, speedup in results:
        print(f"  {num_threads:<10} {elapsed:.2f}s     {speedup:.2f}x")
    print()


if __name__ == "__main__":
    main()
