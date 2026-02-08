"""Rosettes HighlightAccumulator — opt-in profiling for syntax highlighting.

This module provides accumulated metrics during highlighting:
- Per-call language, lexer time, formatter time, total time
- Code length per call
- Aggregate statistics

Zero overhead when disabled (get_accumulator() returns None).

Example:
    from rosettes import highlight
    from rosettes.profiling import profiled_highlight

    # Normal highlight (no overhead)
    html = highlight("def foo(): pass", "python")

    # Profiled highlight (opt-in)
    with profiled_highlight() as metrics:
        html = highlight("def foo(): pass", "python")

    print(metrics.summary())
    # {
    #   "total_ms": 1.2,
    #   "calls": [{"language": "python", "lexer_ms": 0.3, "formatter_ms": 0.8, ...}],
    #   "by_language": {"python": {"count": 1, "total_ms": 1.1}},
    # }

"""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


@dataclass(frozen=True, slots=True)
class HighlightTiming:
    """Timing data for a single highlight call.

    Attributes:
        language: Language that was highlighted.
        lexer_ms: Lexer tokenization time in milliseconds.
        formatter_ms: Formatter formatting time in milliseconds.
        total_ms: Total highlight time in milliseconds.
        code_length: Length of the code string in characters.

    """

    language: str
    lexer_ms: float
    formatter_ms: float
    total_ms: float
    code_length: int


@dataclass
class HighlightAccumulator:
    """Accumulated metrics during syntax highlighting.

    Opt-in profiling for debugging slow highlighting.
    Zero overhead when disabled (get_accumulator() returns None).

    Attributes:
        calls: List of per-call timing data.
        start_time: Profiling start timestamp.

    """

    calls: list[HighlightTiming] = field(default_factory=list)
    start_time: float = field(default_factory=perf_counter)

    def record(
        self,
        language: str,
        lexer_ms: float,
        formatter_ms: float,
        total_ms: float,
        code_length: int,
    ) -> None:
        """Record a highlight call.

        Args:
            language: Language that was highlighted.
            lexer_ms: Lexer tokenization time in milliseconds.
            formatter_ms: Formatter formatting time in milliseconds.
            total_ms: Total highlight time in milliseconds.
            code_length: Length of the code string.

        """
        self.calls.append(
            HighlightTiming(
                language=language,
                lexer_ms=lexer_ms,
                formatter_ms=formatter_ms,
                total_ms=total_ms,
                code_length=code_length,
            )
        )

    @property
    def total_duration_ms(self) -> float:
        """Total profiling duration in milliseconds."""
        return (perf_counter() - self.start_time) * 1000

    @property
    def call_count(self) -> int:
        """Total number of highlight calls recorded."""
        return len(self.calls)

    def summary(self) -> dict[str, Any]:
        """Get summary of highlight metrics.

        Returns:
            Dict with total_ms, call_count, calls, and by_language breakdown.

        """
        by_language: dict[str, dict[str, Any]] = {}
        for call in self.calls:
            if call.language not in by_language:
                by_language[call.language] = {
                    "count": 0,
                    "total_ms": 0.0,
                    "lexer_ms": 0.0,
                    "formatter_ms": 0.0,
                    "total_chars": 0,
                }
            entry = by_language[call.language]
            entry["count"] += 1
            entry["total_ms"] = round(entry["total_ms"] + call.total_ms, 3)
            entry["lexer_ms"] = round(entry["lexer_ms"] + call.lexer_ms, 3)
            entry["formatter_ms"] = round(entry["formatter_ms"] + call.formatter_ms, 3)
            entry["total_chars"] += call.code_length

        return {
            "total_ms": round(self.total_duration_ms, 2),
            "call_count": self.call_count,
            "by_language": dict(
                sorted(by_language.items(), key=lambda x: x[1]["total_ms"], reverse=True)
            ),
        }


# Module-level ContextVar
_accumulator: ContextVar[HighlightAccumulator | None] = ContextVar(
    "highlight_accumulator",
    default=None,
)


def get_accumulator() -> HighlightAccumulator | None:
    """Get current accumulator (None if profiling disabled).

    Returns:
        Current HighlightAccumulator or None if not in profiled context.

    """
    return _accumulator.get()


@contextmanager
def profiled_highlight() -> Iterator[HighlightAccumulator]:
    """Context manager for profiled highlighting.

    Creates a HighlightAccumulator and makes it available via get_accumulator()
    for the duration of the with block. The highlight() function checks for the
    accumulator and records metrics automatically.

    Yields:
        HighlightAccumulator that will be populated during highlight calls.

    Example:
        with profiled_highlight() as metrics:
            html = highlight("def foo(): pass", "python")
        print(metrics.summary())

    """
    acc = HighlightAccumulator()
    token: Token[HighlightAccumulator | None] = _accumulator.set(acc)
    try:
        yield acc
    finally:
        _accumulator.reset(token)
