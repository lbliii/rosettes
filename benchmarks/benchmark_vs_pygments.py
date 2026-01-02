#!/usr/bin/env python3
"""Benchmark Rosettes vs Pygments.

Run with:
    python -m benchmarks.benchmark_vs_pygments

Or with pytest-benchmark:
    pytest benchmarks/benchmark_vs_pygments.py -v --benchmark-only

Requirements:
    pip install pygments pytest-benchmark
"""

from __future__ import annotations

import statistics
import time
from typing import TYPE_CHECKING

import pytest

from benchmarks.sample_code import (
    GO_CODE,
    JAVASCRIPT_CODE,
    PYTHON_10K,
    PYTHON_LARGE,
    PYTHON_MEDIUM,
    PYTHON_SIMPLE,
    RUST_CODE,
)

if TYPE_CHECKING:
    from collections.abc import Callable

# =============================================================================
# Utility functions
# =============================================================================


def benchmark_function(
    name: str,
    func: Callable[[], object],
    iterations: int = 10,
    warmup: int = 2,
) -> dict:
    """Benchmark a function with warmup and statistics.

    Args:
        name: Name for this benchmark.
        func: Zero-argument callable to benchmark.
        iterations: Number of timed iterations.
        warmup: Number of warmup iterations (not timed).

    Returns:
        Dictionary with timing statistics.
    """
    # Warmup
    for _ in range(warmup):
        func()

    # Timed runs
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "name": name,
        "iterations": iterations,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
        "mean_ms": statistics.mean(times) * 1000,
        "median_ms": statistics.median(times) * 1000,
        "stdev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0,
    }


def print_comparison(rosettes_result: dict, pygments_result: dict) -> None:
    """Print a comparison of two benchmark results."""
    speedup = pygments_result["mean_ms"] / rosettes_result["mean_ms"]

    print(f"\n{'─' * 60}")
    print(f"{'Metric':<20} {'Rosettes':>15} {'Pygments':>15} {'Speedup':>10}")
    print(f"{'─' * 60}")
    print(
        f"{'Mean (ms)':<20} {rosettes_result['mean_ms']:>15.3f} "
        f"{pygments_result['mean_ms']:>15.3f} {speedup:>9.2f}x"
    )
    print(
        f"{'Median (ms)':<20} {rosettes_result['median_ms']:>15.3f} "
        f"{pygments_result['median_ms']:>15.3f}"
    )
    print(
        f"{'Min (ms)':<20} {rosettes_result['min_ms']:>15.3f} "
        f"{pygments_result['min_ms']:>15.3f}"
    )
    print(f"{'─' * 60}")


# =============================================================================
# Pytest-benchmark tests (if pytest-benchmark is available)
# =============================================================================


def _pygments_available() -> bool:
    """Check if Pygments is installed."""
    try:
        import pygments  # noqa: F401

        return True
    except ImportError:
        return False


class TestRosettesPerformance:
    """Benchmark Rosettes highlighting performance."""

    def test_rosettes_python_simple(self, benchmark) -> None:
        """Benchmark Rosettes on simple Python code."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(PYTHON_SIMPLE, "python"))
        assert "rosettes" in result

    def test_rosettes_python_medium(self, benchmark) -> None:
        """Benchmark Rosettes on medium Python code (~50 lines)."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(PYTHON_MEDIUM, "python"))
        assert "rosettes" in result

    def test_rosettes_python_large(self, benchmark) -> None:
        """Benchmark Rosettes on large Python code (~500 lines)."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(PYTHON_LARGE, "python"))
        assert "rosettes" in result

    def test_rosettes_rust(self, benchmark) -> None:
        """Benchmark Rosettes on Rust code."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(RUST_CODE, "rust"))
        assert "rosettes" in result

    def test_rosettes_javascript(self, benchmark) -> None:
        """Benchmark Rosettes on JavaScript code."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(JAVASCRIPT_CODE, "javascript"))
        assert "rosettes" in result

    def test_rosettes_go(self, benchmark) -> None:
        """Benchmark Rosettes on Go code."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(GO_CODE, "go"))
        assert "rosettes" in result


@pytest.mark.skipif(not _pygments_available(), reason="Pygments not installed")
class TestPygmentsPerformance:
    """Benchmark Pygments for comparison."""

    def test_pygments_python_simple(self, benchmark) -> None:
        """Benchmark Pygments on simple Python code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer

        lexer = PythonLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(PYTHON_SIMPLE, lexer, formatter))
        assert "<span" in result

    def test_pygments_python_medium(self, benchmark) -> None:
        """Benchmark Pygments on medium Python code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer

        lexer = PythonLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(PYTHON_MEDIUM, lexer, formatter))
        assert "<span" in result

    def test_pygments_python_large(self, benchmark) -> None:
        """Benchmark Pygments on large Python code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer

        lexer = PythonLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(PYTHON_LARGE, lexer, formatter))
        assert "<span" in result

    def test_pygments_rust(self, benchmark) -> None:
        """Benchmark Pygments on Rust code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import RustLexer

        lexer = RustLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(RUST_CODE, lexer, formatter))
        assert "<span" in result

    def test_pygments_javascript(self, benchmark) -> None:
        """Benchmark Pygments on JavaScript code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import JavascriptLexer as JavaScriptLexer

        lexer = JavaScriptLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(JAVASCRIPT_CODE, lexer, formatter))
        assert "<span" in result

    def test_pygments_go(self, benchmark) -> None:
        """Benchmark Pygments on Go code."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import GoLexer

        lexer = GoLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(GO_CODE, lexer, formatter))
        assert "<span" in result


class TestParallelPerformance:
    """Benchmark parallel highlighting with highlight_many()."""

    def test_rosettes_highlight_many_8_blocks(self, benchmark) -> None:
        """Benchmark highlight_many() with 8 code blocks."""
        from rosettes import highlight_many

        blocks = [
            (PYTHON_SIMPLE, "python"),
            (RUST_CODE, "rust"),
            (JAVASCRIPT_CODE, "javascript"),
            (GO_CODE, "go"),
            (PYTHON_MEDIUM, "python"),
            (RUST_CODE, "rust"),
            (JAVASCRIPT_CODE, "javascript"),
            (PYTHON_SIMPLE, "python"),
        ]
        results = benchmark(lambda: highlight_many(blocks))
        assert len(results) == 8

    def test_rosettes_highlight_many_50_blocks(self, benchmark) -> None:
        """Benchmark highlight_many() with 50 code blocks."""
        from rosettes import highlight_many

        blocks = [
            (PYTHON_MEDIUM, "python"),
            (RUST_CODE, "rust"),
            (JAVASCRIPT_CODE, "javascript"),
            (GO_CODE, "go"),
        ] * 12 + [(PYTHON_SIMPLE, "python"), (RUST_CODE, "rust")]

        results = benchmark(lambda: highlight_many(blocks))
        assert len(results) == 50

    @pytest.mark.skipif(not _pygments_available(), reason="Pygments not installed")
    def test_pygments_sequential_8_blocks(self, benchmark) -> None:
        """Benchmark Pygments sequential highlighting (8 blocks)."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import GoLexer, JavascriptLexer, PythonLexer, RustLexer

        formatter = HtmlFormatter()
        blocks = [
            (PYTHON_SIMPLE, PythonLexer()),
            (RUST_CODE, RustLexer()),
            (JAVASCRIPT_CODE, JavascriptLexer()),
            (GO_CODE, GoLexer()),
            (PYTHON_MEDIUM, PythonLexer()),
            (RUST_CODE, RustLexer()),
            (JAVASCRIPT_CODE, JavascriptLexer()),
            (PYTHON_SIMPLE, PythonLexer()),
        ]

        def highlight_all():
            return [highlight(code, lexer, formatter) for code, lexer in blocks]

        results = benchmark(highlight_all)
        assert len(results) == 8


@pytest.mark.slow
class TestLargeFilePerformance:
    """Benchmark performance on large files (10K+ lines)."""

    def test_rosettes_10k_lines(self, benchmark) -> None:
        """Benchmark Rosettes on 10,000 line Python file."""
        from rosettes import highlight

        result = benchmark(lambda: highlight(PYTHON_10K, "python"))
        assert "rosettes" in result

    @pytest.mark.skipif(not _pygments_available(), reason="Pygments not installed")
    def test_pygments_10k_lines(self, benchmark) -> None:
        """Benchmark Pygments on 10,000 line Python file."""
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer

        lexer = PythonLexer()
        formatter = HtmlFormatter()
        result = benchmark(lambda: highlight(PYTHON_10K, lexer, formatter))
        assert "<span" in result


# =============================================================================
# CLI runner (no pytest-benchmark required)
# =============================================================================


def run_cli_benchmark() -> None:
    """Run benchmarks from command line without pytest-benchmark."""
    print("=" * 70)
    print("ROSETTES vs PYGMENTS BENCHMARK")
    print("=" * 70)

    # Check Pygments availability
    try:
        from pygments import highlight as pygments_highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import PythonLexer

        has_pygments = True
    except ImportError:
        has_pygments = False
        print("\n⚠️  Pygments not installed. Install with: pip install pygments")
        print("    Running Rosettes-only benchmarks.\n")

    from rosettes import highlight as rosettes_highlight
    from rosettes import highlight_many

    # Test configurations
    configs = [
        ("Python (simple, ~2 lines)", PYTHON_SIMPLE, "python"),
        ("Python (medium, ~50 lines)", PYTHON_MEDIUM, "python"),
        ("Python (large, ~500 lines)", PYTHON_LARGE, "python"),
        ("Rust (~40 lines)", RUST_CODE, "rust"),
        ("JavaScript (~50 lines)", JAVASCRIPT_CODE, "javascript"),
        ("Go (~45 lines)", GO_CODE, "go"),
    ]

    all_results = []

    for name, code, lang in configs:
        print(f"\n📊 {name}")
        print(f"   Code size: {len(code):,} bytes, {code.count(chr(10)):,} lines")

        # Rosettes benchmark
        rosettes_result = benchmark_function(
            f"Rosettes ({lang})",
            lambda c=code, l=lang: rosettes_highlight(c, l),
            iterations=20,
        )
        print(f"   Rosettes: {rosettes_result['mean_ms']:.3f}ms (mean)")

        if has_pygments:
            # Pygments benchmark
            lexer = PythonLexer()  # Will be overridden per-language
            if lang == "python":
                lexer = PythonLexer()
            elif lang == "rust":
                from pygments.lexers import RustLexer

                lexer = RustLexer()
            elif lang == "javascript":
                from pygments.lexers import JavascriptLexer as JavaScriptLexer

                lexer = JavaScriptLexer()
            elif lang == "go":
                from pygments.lexers import GoLexer

                lexer = GoLexer()

            formatter = HtmlFormatter()
            pygments_result = benchmark_function(
                f"Pygments ({lang})",
                lambda c=code, lx=lexer, f=formatter: pygments_highlight(c, lx, f),
                iterations=20,
            )
            print(f"   Pygments: {pygments_result['mean_ms']:.3f}ms (mean)")

            speedup = pygments_result["mean_ms"] / rosettes_result["mean_ms"]
            print(f"   Speedup:  {speedup:.2f}x")

            all_results.append(
                {
                    "name": name,
                    "rosettes_ms": rosettes_result["mean_ms"],
                    "pygments_ms": pygments_result["mean_ms"],
                    "speedup": speedup,
                }
            )

    # Parallel benchmark
    print("\n" + "=" * 70)
    print("PARALLEL HIGHLIGHTING (highlight_many)")
    print("=" * 70)

    blocks = [
        (PYTHON_MEDIUM, "python"),
        (RUST_CODE, "rust"),
        (JAVASCRIPT_CODE, "javascript"),
        (GO_CODE, "go"),
    ] * 2  # 8 blocks

    print(f"\n📊 8 mixed code blocks")

    rosettes_result = benchmark_function(
        "Rosettes highlight_many",
        lambda: highlight_many(blocks),
        iterations=20,
    )
    print(f"   Rosettes (parallel): {rosettes_result['mean_ms']:.3f}ms")

    if has_pygments:
        from pygments.lexers import GoLexer, JavascriptLexer, RustLexer

        pygments_blocks = [
            (PYTHON_MEDIUM, PythonLexer()),
            (RUST_CODE, RustLexer()),
            (JAVASCRIPT_CODE, JavascriptLexer()),
            (GO_CODE, GoLexer()),
        ] * 2

        formatter = HtmlFormatter()
        pygments_result = benchmark_function(
            "Pygments sequential",
            lambda: [pygments_highlight(c, lx, formatter) for c, lx in pygments_blocks],
            iterations=20,
        )
        print(f"   Pygments (sequential): {pygments_result['mean_ms']:.3f}ms")
        speedup = pygments_result["mean_ms"] / rosettes_result["mean_ms"]
        print(f"   Speedup: {speedup:.2f}x")

    # Large file benchmark
    print("\n" + "=" * 70)
    print("LARGE FILE (10,000 lines Python)")
    print("=" * 70)
    print(f"\n   Code size: {len(PYTHON_10K):,} bytes")

    rosettes_result = benchmark_function(
        "Rosettes (10K lines)",
        lambda: rosettes_highlight(PYTHON_10K, "python"),
        iterations=5,
    )
    print(f"   Rosettes: {rosettes_result['mean_ms']:.1f}ms")

    if has_pygments:
        lexer = PythonLexer()
        formatter = HtmlFormatter()
        pygments_result = benchmark_function(
            "Pygments (10K lines)",
            lambda: pygments_highlight(PYTHON_10K, lexer, formatter),
            iterations=5,
        )
        print(f"   Pygments: {pygments_result['mean_ms']:.1f}ms")
        speedup = pygments_result["mean_ms"] / rosettes_result["mean_ms"]
        print(f"   Speedup: {speedup:.2f}x")

    # Summary table
    if has_pygments and all_results:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"\n{'Test':<35} {'Rosettes':>10} {'Pygments':>10} {'Speedup':>10}")
        print("-" * 70)
        for r in all_results:
            print(
                f"{r['name']:<35} {r['rosettes_ms']:>9.2f}ms {r['pygments_ms']:>9.2f}ms "
                f"{r['speedup']:>9.2f}x"
            )
        avg_speedup = sum(r["speedup"] for r in all_results) / len(all_results)
        print("-" * 70)
        print(f"{'Average speedup':<35} {'':<21} {avg_speedup:>9.2f}x")

    print("\n" + "=" * 70)
    print("✅ Benchmark complete")
    print("=" * 70)


if __name__ == "__main__":
    run_cli_benchmark()

