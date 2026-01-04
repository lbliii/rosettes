"""Shared fixtures for lexer tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from rosettes import get_lexer

# High-priority languages from RFC
HIGH_PRIORITY_LANGUAGES = [
    "kida",
    "python",
    "javascript",
    "typescript",
    "rust",
    "go",
    "yaml",
    "json",
    "bash",
    "html",
    "css",
    "sql",
    "markdown",
    "java",
    "c",
    "cpp",
    "jinja",
]

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

# Extension mapping for finding source files
EXTENSIONS = [
    ".py", ".js", ".ts", ".rs", ".go", ".java", ".kt", ".swift", ".rb", ".pl",
    ".lua", ".scala", ".ex", ".hs", ".nim", ".zig", ".v", ".dart", ".gleam",
    ".yaml", ".json", ".php", ".sh", ".sql", ".toml", ".xml", ".html", ".css",
    ".md", ".kida", ".c", ".cpp", ".h", ".hpp", ".dockerfile", ".graphql", ".tf",
    ".groovy", ".r", ".jl", ".ini", ".csv", ".diff", ".makefile", ".nginx",
    ".proto", ".mojo", ".triton", ".cu", ".stan", ".pkl", ".cue", ".clj",
    ".jinja", ".tree", ".ps1", ".txt"
]


@pytest.fixture
def lexer(request):
    """Parametrized fixture to get any lexer by name."""
    language = request.param
    return get_lexer(language)


@pytest.fixture
def load_fixture():
    """Load fixture source and expected tokens.
    
    Usage:
        def test_something(load_fixture):
            code, expected_tokens = load_fixture("python", "keywords")
    """
    def _load(language: str, name: str) -> tuple[str, list[dict]]:
        lang_dir = FIXTURES_DIR / language
        
        # Find source file (try common extensions)
        source_file = None
        for ext in EXTENSIONS:
            candidate = lang_dir / f"{name}{ext}"
            if candidate.exists():
                source_file = candidate
                break
        
        if source_file is None:
            pytest.skip(f"Fixture {name} not found for {language}")
        
        tokens_file = lang_dir / f"{name}.tokens.json"
        if not tokens_file.exists():
            pytest.skip(f"Tokens file not found: {tokens_file}")
        
        code = source_file.read_text(encoding="utf-8")
        expected_tokens = json.loads(tokens_file.read_text(encoding="utf-8"))
        
        return code, expected_tokens
    
    return _load
