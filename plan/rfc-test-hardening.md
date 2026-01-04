# RFC: Test Coverage and Hardening for Rosettes

| Field | Value |
|-------|-------|
| **Status** | Draft |
| **Created** | 2026-01-04 |
| **Updated** | 2026-01-04 |
| **Author** | Bengal Team |
| **Scope** | Quality Assurance |
| **Goal** | Strengthen test coverage and add property-based testing for lexer correctness guarantees |

## Summary

Improve Rosettes test coverage from 53% to 80%+ with a focus on:
1. Property-based testing for lexer invariants
2. Expanded lexer tests for high-traffic languages
3. Missing fixture files for golden tests
4. Theme/CSS generation coverage

## Motivation

### Current State

**Test results**: 320 passed, 28 skipped, 1 warning

**Coverage by area**:

| Module | Coverage | Gap Analysis |
|--------|----------|--------------|
| Core (`__init__.py`, `_registry.py`, etc.) | 85-100% | ✅ Good |
| Security (`test_redos.py`, `test_escaping.py`) | 100% | ✅ Strong |
| Formatters | 88-100% | ✅ Good |
| Lexers (average) | 19-85% | ⚠️ Wide variance |
| Themes | 85-88% | 🟡 CSS generation skipped |

### Lexer Coverage Concerns

Only 4 of 54 lexers have dedicated test files:

| Lexer | Has Tests | Coverage |
|-------|-----------|----------|
| Python | ✅ | 85% |
| JavaScript | ✅ | 74% |
| Rust | ✅ | 74% |
| Kida | ✅ | 78% |
| PHP | ❌ | 19% |
| XML | ❌ | 19% |
| TOML | ❌ | 29% |
| Ruby | ❌ | 32% |
| YAML | ❌ | 43% |
| (50 others) | ❌ | 37-62% |

The ReDoS tests cover all lexers with pathological inputs, but don't verify **correctness**.

### Missing Test Infrastructure

**28 tests skipped due to missing fixtures:**

```
SKIPPED: Fixture keywords not found
SKIPPED: Fixture strings not found
SKIPPED: Fixture numbers not found
...
```

**Theme tests skipped:**

```
SKIPPED: Palette CSS generation not available
SKIPPED: Palette github not available
```

**Pytest marker not registered:**

```
PytestUnknownMarkWarning: Unknown pytest.mark.slow
```

### Why This Matters

Rosettes makes **strong guarantees**:
- O(n) performance (no ReDoS)
- Thread-safe tokenization
- Correct highlighting across 54 languages

Without comprehensive tests, we cannot verify the "correct highlighting" claim for most languages.

## Design

### Core Principle: Property-Based Testing

Rather than hand-writing tests for every language construct in 54 languages, use **property-based testing** to verify invariants that must hold for ALL lexers:

#### Invariant 1: Token Concatenation

```python
# For any valid code, concatenating all token values reproduces the original
def test_token_concatenation(lexer, code):
    tokens = list(lexer.tokenize(code))
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == code
```

**Why this matters**: Ensures no characters are dropped or duplicated during tokenization.

#### Invariant 2: Token Positions

```python
# All tokens have valid line/column positions
def test_token_positions(lexer, code):
    for token in lexer.tokenize(code):
        assert token.line >= 1
        assert token.column >= 1
```

#### Invariant 3: No Empty Tokens

```python
# Tokens should not be empty (except possibly at EOF)
def test_no_empty_tokens(lexer, code):
    tokens = list(lexer.tokenize(code))
    for token in tokens[:-1]:  # Allow empty at end
        assert len(token.value) > 0
```

#### Invariant 4: Monotonic Positions

```python
# Token positions should advance (within same line)
def test_monotonic_columns(lexer, code):
    prev_line, prev_col = 0, 0
    for token in lexer.tokenize(code):
        if token.line == prev_line:
            assert token.column >= prev_col + len(prev_value)
        prev_line, prev_col = token.line, token.column
```

### Test Categories

| Category | Purpose | Tools |
|----------|---------|-------|
| **Property Tests** | Verify universal invariants | `hypothesis` |
| **Golden Tests** | Verify expected tokenization | Fixtures |
| **Regression Tests** | Capture bugs once found | Inline code |
| **Security Tests** | ReDoS, XSS prevention | Existing |
| **Performance Tests** | O(n) guarantee | Existing + benchmarks |

## Implementation

### Phase 1: Infrastructure (30 min)

#### 1.1 Register pytest marks

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = ["-ra", "-q", "--strict-markers"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "property: property-based tests (may take longer)",
]
```

#### 1.2 Add hypothesis dependency

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-cov>=6.0.0",
    "ruff>=0.14.0",
    "hypothesis>=6.100.0",  # NEW
]
```

### Phase 2: Property Tests (2 hours)

Create `tests/properties/test_lexer_invariants.py`:

```python
"""Property-based tests for lexer invariants.

These tests verify properties that must hold for ALL lexers,
regardless of language. Uses hypothesis to generate diverse inputs.
"""
from __future__ import annotations

import pytest
from hypothesis import given, settings, strategies as st

from rosettes import get_lexer, list_languages, TokenType


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
        assert len(token.value) > 0, (
            f"Empty token at position {i} in {language}: {token}"
        )


@pytest.mark.property
@pytest.mark.parametrize("language", list_languages()[:10])  # Subset for speed
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
```

### Phase 3: High-Priority Lexer Tests (2 hours)

Add focused tests for the highest-traffic languages with lowest coverage:

#### 3.1 `tests/lexers/test_yaml_sm.py`

```python
"""Tests for YAML lexer (43% coverage → target 75%)."""
from __future__ import annotations

import pytest
from rosettes import TokenType, get_lexer


class TestYamlBasics:
    """Test basic YAML constructs."""

    def test_key_value(self) -> None:
        lexer = get_lexer("yaml")
        code = "key: value"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.NAME in types or TokenType.NAME_TAG in types

    def test_nested_mapping(self) -> None:
        lexer = get_lexer("yaml")
        code = """
parent:
  child: value
  sibling: other
"""
        tokens = list(lexer.tokenize(code))
        assert len(tokens) > 0
        reconstructed = "".join(t.value for t in tokens)
        assert reconstructed == code

    def test_list_items(self) -> None:
        lexer = get_lexer("yaml")
        code = """
items:
  - first
  - second
  - third
"""
        tokens = list(lexer.tokenize(code))
        # Should have PUNCTUATION for dashes
        values = [t.value for t in tokens]
        assert "-" in values

    def test_multiline_string(self) -> None:
        lexer = get_lexer("yaml")
        code = """
description: |
  This is a multiline
  string value
"""
        tokens = list(lexer.tokenize(code))
        reconstructed = "".join(t.value for t in tokens)
        assert reconstructed == code

    def test_anchors_and_aliases(self) -> None:
        lexer = get_lexer("yaml")
        code = """
defaults: &defaults
  timeout: 30

production:
  <<: *defaults
  timeout: 60
"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "&defaults" in values or "&" in values

    def test_comments(self) -> None:
        lexer = get_lexer("yaml")
        code = "key: value  # this is a comment"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.COMMENT_SINGLE in types


class TestYamlEdgeCases:
    """Test YAML edge cases."""

    def test_empty_value(self) -> None:
        lexer = get_lexer("yaml")
        code = "empty:"
        tokens = list(lexer.tokenize(code))
        assert len(tokens) > 0

    def test_quoted_strings(self) -> None:
        lexer = get_lexer("yaml")
        code = 'quoted: "value with spaces"'
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.STRING in types or TokenType.STRING_DOUBLE in types

    def test_boolean_values(self) -> None:
        lexer = get_lexer("yaml")
        code = """
enabled: true
disabled: false
"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "true" in values or "True" in values

    def test_numeric_values(self) -> None:
        lexer = get_lexer("yaml")
        code = """
integer: 42
float: 3.14
negative: -10
"""
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.NUMBER in types or TokenType.NUMBER_INTEGER in types
```

#### 3.2 `tests/lexers/test_php_sm.py`

```python
"""Tests for PHP lexer (19% coverage → target 70%)."""
from __future__ import annotations

import pytest
from rosettes import TokenType, get_lexer


class TestPhpBasics:
    """Test basic PHP constructs."""

    def test_php_tags(self) -> None:
        lexer = get_lexer("php")
        code = "<?php echo 'hello'; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "<?php" in values or "<?" in values

    def test_variables(self) -> None:
        lexer = get_lexer("php")
        code = "<?php $name = 'test'; ?>"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.NAME_VARIABLE in types or any(
            t.value.startswith("$") for t in tokens
        )

    def test_functions(self) -> None:
        lexer = get_lexer("php")
        code = "<?php function greet($name) { return 'Hello ' . $name; } ?>"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.KEYWORD_DECLARATION in types or TokenType.KEYWORD in types

    def test_class_definition(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
class User {
    public $name;
    
    public function __construct($name) {
        $this->name = $name;
    }
}
?>"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "class" in values

    def test_arrays(self) -> None:
        lexer = get_lexer("php")
        code = "<?php $arr = ['a' => 1, 'b' => 2]; ?>"
        tokens = list(lexer.tokenize(code))
        reconstructed = "".join(t.value for t in tokens)
        assert reconstructed == code

    def test_heredoc(self) -> None:
        lexer = get_lexer("php")
        code = '''<?php
$text = <<<EOT
This is heredoc
text content
EOT;
?>'''
        tokens = list(lexer.tokenize(code))
        reconstructed = "".join(t.value for t in tokens)
        assert reconstructed == code


class TestPhpEdgeCases:
    """Test PHP edge cases."""

    def test_string_interpolation(self) -> None:
        lexer = get_lexer("php")
        code = '<?php echo "Hello $name"; ?>'
        tokens = list(lexer.tokenize(code))
        assert len(tokens) > 0

    def test_namespace(self) -> None:
        lexer = get_lexer("php")
        code = "<?php namespace App\\Models; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "namespace" in values

    def test_comments(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
// Single line comment
/* Multi-line
   comment */
# Shell-style comment
?>"""
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.COMMENT_SINGLE in types or TokenType.COMMENT_MULTILINE in types
```

### Phase 4: Theme Tests (1 hour)

Fix and expand `tests/themes/test_css_generation.py`:

```python
"""Tests for CSS generation from palettes."""
from __future__ import annotations

import pytest

from rosettes.themes import list_palettes, get_palette


class TestPaletteRegistry:
    """Test palette registry."""

    def test_list_palettes(self) -> None:
        """Should list available palettes."""
        palettes = list_palettes()
        assert isinstance(palettes, list)
        assert len(palettes) >= 1
        assert "bengal-tiger" in palettes

    def test_get_palette(self) -> None:
        """Should get palette by name."""
        palette = get_palette("bengal-tiger")
        assert palette is not None
        assert hasattr(palette, "name")


class TestCssGeneration:
    """Test CSS generation from palettes."""

    @pytest.mark.parametrize("palette_name", list_palettes())
    def test_css_generation(self, palette_name: str) -> None:
        """CSS should be generated for all palettes."""
        palette = get_palette(palette_name)
        css = palette.generate_css()

        assert isinstance(css, str)
        assert len(css) > 0
        # Should have CSS rules
        assert "{" in css and "}" in css
        # Should have color values
        assert "#" in css or "rgb" in css

    @pytest.mark.parametrize("palette_name", list_palettes())
    def test_css_contains_core_token_types(self, palette_name: str) -> None:
        """CSS should contain styles for core token types."""
        palette = get_palette(palette_name)
        css = palette.generate_css()

        # Check for common token class patterns
        # (either semantic or pygments style)
        core_patterns = [
            (".syntax-", ".s", ".k"),  # semantic or pygments
        ]
        
        has_any = any(
            any(p in css for p in patterns)
            for patterns in core_patterns
        )
        assert has_any, f"CSS missing core token styles: {css[:200]}..."

    def test_css_valid_syntax(self) -> None:
        """Generated CSS should have valid syntax."""
        palette = get_palette("bengal-tiger")
        css = palette.generate_css()

        # Basic syntax checks
        open_braces = css.count("{")
        close_braces = css.count("}")
        assert open_braces == close_braces, "Mismatched braces in CSS"
        
        # Should not have obvious errors
        assert "undefined" not in css.lower()
        assert "null" not in css.lower()
```

### Phase 5: Fix Skipped Tests (1 hour)

#### 5.1 Create missing fixture files

Structure for `tests/fixtures/`:

```
tests/fixtures/
├── javascript/
│   ├── keywords.js
│   ├── keywords.tokens
│   ├── strings.js
│   ├── strings.tokens
│   └── ...
├── python/
│   ├── keywords.py
│   ├── keywords.tokens
│   └── ...
└── ...
```

Example `tests/fixtures/python/keywords.py`:

```python
# Test: Python keywords
if True:
    pass
elif False:
    pass
else:
    pass

for x in range(10):
    continue
    break

while True:
    pass

def func():
    return None

class MyClass:
    pass

try:
    raise Exception
except Exception:
    pass
finally:
    pass

with open("file") as f:
    pass

import os
from sys import path

async def async_func():
    await something()

lambda x: x + 1

assert True
del x
global y
nonlocal z
yield value
```

### Phase 6: CI Integration (30 min)

Update CI to run property tests:

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      
      - name: Run fast tests
        run: uv run pytest tests/ -m "not slow and not property"
        
      - name: Run property tests
        run: uv run pytest tests/ -m property --hypothesis-seed=0
        
      - name: Run slow tests (optional)
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: uv run pytest tests/ -m slow
```

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| **Overall coverage** | 80%+ | `pytest --cov` |
| **Lexer average coverage** | 70%+ | Per-lexer coverage |
| **Property tests pass** | 100% | All invariants hold |
| **No skipped tests** | 0 | All fixtures present |
| **Theme tests pass** | 100% | CSS generation works |
| **CI green** | 100% | All jobs pass |

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| 1: Infrastructure | 30 min | pytest config, hypothesis dep |
| 2: Property tests | 2 hours | `test_lexer_invariants.py` |
| 3: Lexer tests | 2 hours | YAML, PHP, TOML lexer tests |
| 4: Theme tests | 1 hour | CSS generation tests |
| 5: Fixtures | 1 hour | Missing fixture files |
| 6: CI | 30 min | Workflow updates |
| **Total** | ~7 hours | |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Property tests find bugs | Medium | Fix bugs, add regression tests |
| Hypothesis slow on CI | Low | Use `--hypothesis-seed=0` for determinism |
| Some lexers fail invariants | Medium | Fix lexers or document exceptions |
| Coverage target too aggressive | Low | Adjust to 75% if needed |

## Future Considerations

### Fuzzing

Consider integrating with [OSS-Fuzz](https://github.com/google/oss-fuzz) or [Atheris](https://github.com/google/atheris) for continuous security fuzzing:

```python
import atheris
import sys

def fuzz_lexer(data):
    """Fuzz target for lexer testing."""
    fdp = atheris.FuzzedDataProvider(data)
    code = fdp.ConsumeUnicodeNoSurrogates(1000)
    lang = fdp.PickValueInList(list_languages())
    
    lexer = get_lexer(lang)
    tokens = list(lexer.tokenize(code))
    
    # Invariant check
    reconstructed = "".join(t.value for t in tokens)
    assert reconstructed == code

atheris.Setup(sys.argv, fuzz_lexer)
atheris.Fuzz()
```

### Mutation Testing

Add mutation testing to verify test effectiveness:

```toml
[dependency-groups]
dev = [
    # ... existing ...
    "mutmut>=2.4.0",
]
```

```bash
uv run mutmut run --paths-to-mutate=src/rosettes/lexers/
```

### Performance Benchmarks

Add performance regression tests:

```python
@pytest.mark.benchmark
def test_python_lexer_performance(benchmark):
    """Python lexer should tokenize 10K lines in < 50ms."""
    lexer = get_lexer("python")
    code = "x = 1\n" * 10_000
    
    result = benchmark(lambda: list(lexer.tokenize(code)))
    
    assert benchmark.stats["mean"] < 0.05  # 50ms
```

## References

- Current test suite: `tests/`
- Coverage report: `uv run pytest --cov=rosettes --cov-report=term-missing`
- Hypothesis documentation: https://hypothesis.readthedocs.io/
- Rosettes design philosophy: `src/rosettes/__init__.py` docstring

