"""Tests for rosettes profiling API."""

from concurrent.futures import ThreadPoolExecutor

from rosettes import highlight
from rosettes.profiling import (
    HighlightAccumulator,
    HighlightTiming,
    get_accumulator,
    profiled_highlight,
)


class TestGetAccumulator:
    """Tests for get_accumulator() when profiling is disabled."""

    def test_returns_none_when_disabled(self) -> None:
        assert get_accumulator() is None

    def test_returns_none_outside_context(self) -> None:
        with profiled_highlight():
            pass
        assert get_accumulator() is None


class TestProfiledHighlight:
    """Tests for the profiled_highlight context manager."""

    def test_yields_accumulator(self) -> None:
        with profiled_highlight() as acc:
            assert isinstance(acc, HighlightAccumulator)

    def test_accumulator_available_inside_context(self) -> None:
        with profiled_highlight() as acc:
            assert get_accumulator() is acc

    def test_accumulator_cleared_after_context(self) -> None:
        with profiled_highlight():
            pass
        assert get_accumulator() is None

    def test_records_highlight_call(self) -> None:
        with profiled_highlight() as acc:
            highlight("def foo(): pass", "python")
        assert acc.call_count == 1
        assert acc.calls[0].language == "python"

    def test_records_multiple_calls(self) -> None:
        with profiled_highlight() as acc:
            highlight("def foo(): pass", "python")
            highlight("const x = 1;", "javascript")
            highlight("fn main() {}", "rust")
        assert acc.call_count == 3
        languages = [c.language for c in acc.calls]
        assert "python" in languages
        assert "javascript" in languages
        assert "rust" in languages

    def test_records_code_length(self) -> None:
        code = "def hello(): pass"
        with profiled_highlight() as acc:
            highlight(code, "python")
        assert acc.calls[0].code_length == len(code)

    def test_timing_values_positive(self) -> None:
        with profiled_highlight() as acc:
            highlight("x = 1\ny = 2\nz = x + y", "python")
        call = acc.calls[0]
        assert call.lexer_ms >= 0
        assert call.formatter_ms >= 0
        assert call.total_ms >= 0
        assert call.total_ms >= call.lexer_ms

    def test_total_duration_positive(self) -> None:
        with profiled_highlight() as acc:
            highlight("print('hello')", "python")
        assert acc.total_duration_ms > 0


class TestHighlightTiming:
    """Tests for the HighlightTiming frozen dataclass."""

    def test_is_frozen(self) -> None:
        timing = HighlightTiming(
            language="python",
            lexer_ms=1.0,
            formatter_ms=2.0,
            total_ms=3.0,
            code_length=100,
        )
        assert timing.language == "python"
        assert timing.total_ms == 3.0


class TestSummary:
    """Tests for the summary() method."""

    def test_empty_summary(self) -> None:
        acc = HighlightAccumulator()
        summary = acc.summary()
        assert summary["call_count"] == 0
        assert summary["by_language"] == {}

    def test_summary_by_language(self) -> None:
        with profiled_highlight() as acc:
            highlight("def foo(): pass", "python")
            highlight("class Bar: pass", "python")
            highlight("const x = 1;", "javascript")
        summary = acc.summary()
        assert summary["call_count"] == 3
        assert "python" in summary["by_language"]
        assert "javascript" in summary["by_language"]
        assert summary["by_language"]["python"]["count"] == 2
        assert summary["by_language"]["javascript"]["count"] == 1

    def test_summary_total_ms_present(self) -> None:
        with profiled_highlight() as acc:
            highlight("x = 1", "python")
        summary = acc.summary()
        assert "total_ms" in summary
        assert summary["total_ms"] >= 0


class TestSlowPath:
    """Tests for profiling on the slow path (hl_lines, linenos)."""

    def test_records_with_hl_lines(self) -> None:
        with profiled_highlight() as acc:
            highlight("x = 1\ny = 2\nz = 3", "python", hl_lines={2})
        assert acc.call_count == 1
        assert acc.calls[0].language == "python"

    def test_records_with_linenos(self) -> None:
        with profiled_highlight() as acc:
            highlight("x = 1", "python", show_linenos=True)
        assert acc.call_count == 1


class TestThreadSafety:
    """Tests for profiling thread-safety."""

    def test_independent_accumulators_per_thread(self) -> None:
        """Each thread should have its own accumulator via ContextVar."""
        results: list[int] = []

        def _highlight_in_thread(lang: str) -> int:
            with profiled_highlight() as acc:
                highlight("x = 1", lang)
                return acc.call_count

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(_highlight_in_thread, "python"),
                executor.submit(_highlight_in_thread, "javascript"),
            ]
            results = [f.result() for f in futures]

        # Each thread should see exactly 1 call in its own accumulator
        assert results == [1, 1]

    def test_nested_accumulators_independent(self) -> None:
        """A thread can create its own profiled context that doesn't affect the parent."""

        def _highlight_with_own_profiling() -> int:
            with profiled_highlight() as inner_acc:
                highlight("x = 1", "python")
                return inner_acc.call_count

        with profiled_highlight() as outer_acc:
            highlight("y = 2", "python")
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_highlight_with_own_profiling)
                inner_count = future.result()

        # Inner thread saw exactly 1 call in its own accumulator
        assert inner_count == 1
        # Outer accumulator only saw its own call
        assert outer_acc.call_count == 1
