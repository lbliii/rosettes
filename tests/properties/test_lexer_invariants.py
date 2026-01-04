"""Property-based tests for lexer invariants.

These tests verify properties that must hold for ALL lexers,
regardless of language. Uses hypothesis to generate diverse inputs.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings, strategies as st

from rosettes import TokenType, get_lexer, list_languages


# Strategy: Generate plausible source code
code_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S", "Z"),
        whitelist_characters="\n\t",
    ),
    min_size=0,
    max_size=1000,
)

# Strategy: Random bytes (stress test)
random_bytes_strategy = st.binary(min_size=0, max_size=500).map(
    lambda b: b.decode("utf-8", errors="replace")
)


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages())
@given(code=code_strategy)
@settings(max_examples=50, deadline=1000)
def test_token_concatenation_reconstructs_input(language: str, code: str) -> None:
    """Concatenating all token values must reproduce the original input."""
    lexer = get_lexer(language)
    tokens = list(lexer.tokenize(code))
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == code, (
        f"Token concatenation mismatch for {language}:\n"
        f"Input:  {code!r}\n"
        f"Output: {reconstructed!r}\n"
        f"Tokens: {[(t.type.name, t.value) for t in tokens]}"
    )


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages())
@given(code=code_strategy)
@settings(max_examples=50, deadline=1000)
def test_all_tokens_have_valid_positions(language: str, code: str) -> None:
    """All tokens must have line >= 1 and column >= 1."""
    lexer = get_lexer(language)
    for token in lexer.tokenize(code):
        assert token.line >= 1, f"Invalid line {token.line} for {token}"
        assert token.column >= 1, f"Invalid column {token.column} for {token}"


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages())
@given(code=code_strategy)
@settings(max_examples=50, deadline=1000)
def test_no_empty_internal_tokens(language: str, code: str) -> None:
    """Internal tokens should not be empty."""
    lexer = get_lexer(language)
    tokens = list(lexer.tokenize(code))

    # All tokens except possibly the last should have content
    for i, token in enumerate(tokens[:-1]):
        assert len(token.value) > 0, f"Empty token at position {i} in {language}: {token}"


# Subset of languages for random bytes stress test (55 total, test 10 for speed)
RANDOM_BYTES_LANGUAGES = list_languages()[:10]


@pytest.mark.property
@pytest.mark.parametrize("language", RANDOM_BYTES_LANGUAGES)
@given(code=random_bytes_strategy)
@settings(max_examples=20, deadline=2000)
def test_lexer_handles_random_bytes(language: str, code: str) -> None:
    """Lexer should not crash on arbitrary UTF-8 input."""
    lexer = get_lexer(language)
    # Should complete without exception
    tokens = list(lexer.tokenize(code))
    # Token concatenation should still work
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == code


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages())
def test_empty_input_produces_valid_output(language: str) -> None:
    """Empty input should produce empty or whitespace-only tokens."""
    lexer = get_lexer(language)
    tokens = list(lexer.tokenize(""))
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == ""


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages())
def test_single_newline_tokenizes(language: str) -> None:
    """Single newline should tokenize correctly."""
    lexer = get_lexer(language)
    tokens = list(lexer.tokenize("\n"))
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == "\n"


class TestTokenTypeConsistency:
    """Verify token types are used consistently."""

    @pytest.mark.parametrize("language", list_languages())
    def test_all_tokens_have_valid_type(self, language: str) -> None:
        """All tokens should have a valid TokenType."""
        lexer = get_lexer(language)
        code = "x = 1 + 2"  # Simple expression most languages handle

        for token in lexer.tokenize(code):
            assert isinstance(token.type, TokenType), (
                f"Invalid token type {token.type} for {language}"
            )

