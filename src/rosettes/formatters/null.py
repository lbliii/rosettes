"""Null formatter for Rosettes.

Does nothing but return the raw text. Useful for timing or as a fallback.
Thread-safe and optimized for streaming.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rosettes._config import FormatConfig
    from rosettes._types import Token, TokenType


@dataclass(frozen=True, slots=True)
class NullFormatter:
    """Formatter that yields raw token values without any styling.

    Thread-safe: immutable dataclass with no shared state.
    """

    @property
    def name(self) -> str:
        return "null"

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Format tokens by yielding their raw values."""
        for token in tokens:
            yield token.value

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Fast formatting — just yield raw values."""
        for _, value in tokens:
            yield value

    def format_string(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> str:
        """Format tokens and return as a single string."""
        return "".join(self.format(tokens, config))

    def format_string_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> str:
        """Fast format and return as a single string."""
        return "".join(self.format_fast(tokens, config))

