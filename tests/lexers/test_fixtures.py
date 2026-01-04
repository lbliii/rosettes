"""Unified test runner for all lexer fixtures.

This test file discovers and validates all fixtures across all languages.
Complements language-specific tests in test_*_sm.py files.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rosettes import get_lexer

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def discover_fixtures():
    """Discover all fixture pairs (source + tokens).
    
    Returns:
        List of tuples: (language, fixture_name, source_file, tokens_file)
    """
    fixtures = []
    if not FIXTURES_DIR.exists():
        return fixtures
    
    for lang_dir in sorted(FIXTURES_DIR.iterdir()):
        if not lang_dir.is_dir():
            continue
        language = lang_dir.name
        
        for tokens_file in sorted(lang_dir.glob("*.tokens.json")):
            name = tokens_file.stem.replace(".tokens", "")
            
            # Find corresponding source file (try common extensions)
            source_file = None
            for ext in [
                ".py", ".js", ".ts", ".rs", ".go", ".java", ".kt", ".swift",
                ".rb", ".pl", ".lua", ".scala", ".ex", ".hs", ".nim", ".zig",
                ".v", ".dart", ".gleam", ".yaml", ".json", ".php", ".sh",
                ".sql", ".toml", ".xml", ".html", ".css", ".md", ".kida",
                ".c", ".cpp", ".h", ".hpp", ".dockerfile", ".graphql", ".tf",
                ".groovy", ".r", ".jl", ".ini", ".csv", ".diff", ".makefile",
                ".nginx", ".proto", ".mojo", ".triton", ".cu", ".stan", ".pkl",
                ".cue", ".clj", ".jinja", ".tree", ".ps1", ".txt"
            ]:
                candidate = lang_dir / f"{name}{ext}"
                if candidate.exists():
                    source_file = candidate
                    break
            
            if source_file:
                fixtures.append((language, name, source_file, tokens_file))
    
    return fixtures


FIXTURES = discover_fixtures()


@pytest.mark.parametrize("language,name,source_file,tokens_file", FIXTURES)
def test_fixture_token_types(language, name, source_file, tokens_file):
    """Verify token types match expected fixture."""
    lexer = get_lexer(language)
    source = source_file.read_text(encoding="utf-8")
    
    try:
        expected_json = tokens_file.read_text(encoding="utf-8")
        expected = json.loads(expected_json)
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON in {tokens_file}: {e}")
    
    actual = list(lexer.tokenize(source))
    
    # First verify count matches
    assert len(actual) == len(expected), (
        f"Token count mismatch for {language}/{name}: "
        f"got {len(actual)}, expected {len(expected)}\n"
        f"Source: {source_file}\n"
        f"Tokens: {tokens_file}"
    )
    
    # Then verify each token
    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act.type.name == exp["type"], (
            f"Token {i} type mismatch in {language}/{name}: "
            f"got {act.type.name}, expected {exp['type']} "
            f"for value {act.value!r} at line {act.line}, column {act.column}"
        )
        assert act.value == exp["value"], (
            f"Token {i} value mismatch in {language}/{name}: "
            f"got {act.value!r}, expected {exp['value']!r} "
            f"at line {act.line}, column {act.column}"
        )
        # Optionally verify line/column if present in expected
        if "line" in exp:
            assert act.line == exp["line"], (
                f"Token {i} line mismatch in {language}/{name}: "
                f"got {act.line}, expected {exp['line']}"
            )
        if "column" in exp:
            assert act.column == exp["column"], (
                f"Token {i} column mismatch in {language}/{name}: "
                f"got {act.column}, expected {exp['column']}"
            )


@pytest.mark.parametrize("language,name,source_file,tokens_file", FIXTURES)
def test_fixture_reconstructs(language, name, source_file, tokens_file):
    """Verify tokenization reconstructs original source (invariant check)."""
    lexer = get_lexer(language)
    source = source_file.read_text(encoding="utf-8")
    
    tokens = list(lexer.tokenize(source))
    reconstructed = "".join(t.value for t in tokens)
    
    assert reconstructed == source, (
        f"Reconstruction failed for {language}/{name}: "
        f"source length {len(source)}, reconstructed length {len(reconstructed)}"
    )

