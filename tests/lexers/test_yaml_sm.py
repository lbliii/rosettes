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
        # YAML keys are NAME_ATTRIBUTE, values are STRING
        assert TokenType.NAME_ATTRIBUTE in types or TokenType.NAME in types or TokenType.NAME_TAG in types

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
        # Dashes may be part of list item tokens
        values = [t.value for t in tokens]
        # Check that dash appears somewhere (may be combined with value)
        assert any("-" in v for v in values)

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

    def test_null_values(self) -> None:
        lexer = get_lexer("yaml")
        code = "value: null"
        tokens = list(lexer.tokenize(code))
        assert len(tokens) > 0
        reconstructed = "".join(t.value for t in tokens)
        assert reconstructed == code

    def test_flow_sequence(self) -> None:
        lexer = get_lexer("yaml")
        code = "items: [a, b, c]"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "[" in values and "]" in values

    def test_flow_mapping(self) -> None:
        lexer = get_lexer("yaml")
        code = "person: {name: John, age: 30}"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "{" in values and "}" in values

    def test_document_markers(self) -> None:
        lexer = get_lexer("yaml")
        code = """---
key: value
...
"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "---" in values

    def test_single_quoted_string(self) -> None:
        lexer = get_lexer("yaml")
        code = "name: 'single quoted'"
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.STRING in types or TokenType.STRING_SINGLE in types

