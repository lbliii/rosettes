"""Comprehensive tests for Solidity lexer.

Tests token accuracy for Solidity constructs:
- Keywords (contract, function, mapping, event, etc.)
- Types (address, uint, int, bool, etc.)
- pragma, import, using
- Comments: //, /* */, ///
- Operators: => for function types
- NatSpec /** ... */
"""

from __future__ import annotations

import pytest

from rosettes import TokenType


class TestSolidityKeywords:
    """Test Solidity keyword tokenization."""

    def test_contract_keyword(self, solidity_lexer) -> None:
        """'contract' should be KEYWORD_DECLARATION."""
        tokens = list(solidity_lexer.tokenize("contract"))
        assert tokens[0].type == TokenType.KEYWORD_DECLARATION
        assert tokens[0].value == "contract"

    def test_function_keyword(self, solidity_lexer) -> None:
        """'function' should be KEYWORD_DECLARATION."""
        tokens = list(solidity_lexer.tokenize("function"))
        assert tokens[0].type == TokenType.KEYWORD_DECLARATION

    def test_mapping_keyword(self, solidity_lexer) -> None:
        """'mapping' should be KEYWORD (type constructor)."""
        tokens = list(solidity_lexer.tokenize("mapping"))
        assert tokens[0].type == TokenType.KEYWORD

    def test_event_keyword(self, solidity_lexer) -> None:
        """'event' should be KEYWORD_DECLARATION."""
        tokens = list(solidity_lexer.tokenize("event"))
        assert tokens[0].type == TokenType.KEYWORD_DECLARATION

    def test_emit_keyword(self, solidity_lexer) -> None:
        """'emit' should be KEYWORD."""
        tokens = list(solidity_lexer.tokenize("emit"))
        assert tokens[0].type == TokenType.KEYWORD

    def test_pragma_keyword(self, solidity_lexer) -> None:
        """'pragma' should be KEYWORD_NAMESPACE."""
        tokens = list(solidity_lexer.tokenize("pragma"))
        assert tokens[0].type == TokenType.KEYWORD_NAMESPACE

    def test_public_payable_view(self, solidity_lexer) -> None:
        """'public', 'payable', 'view' should be KEYWORD."""
        code = "public payable view"
        tokens = list(solidity_lexer.tokenize(code))
        values = [t.value for t in tokens if t.type == TokenType.KEYWORD]
        assert "public" in values
        assert "payable" in values
        assert "view" in values


class TestSolidityTypes:
    """Test Solidity type tokenization."""

    def test_address_type(self, solidity_lexer) -> None:
        """'address' should be KEYWORD_TYPE."""
        tokens = list(solidity_lexer.tokenize("address"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE

    def test_uint_type(self, solidity_lexer) -> None:
        """'uint' should be KEYWORD_TYPE."""
        tokens = list(solidity_lexer.tokenize("uint"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE

    def test_bool_type(self, solidity_lexer) -> None:
        """'bool' should be KEYWORD_TYPE."""
        tokens = list(solidity_lexer.tokenize("bool"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE

    def test_uint256_type(self, solidity_lexer) -> None:
        """'uint256' should be KEYWORD_TYPE."""
        tokens = list(solidity_lexer.tokenize("uint256"))
        assert tokens[0].type == TokenType.KEYWORD_TYPE


class TestSolidityComments:
    """Test Solidity comment tokenization."""

    def test_line_comment(self, solidity_lexer) -> None:
        """// comments should be COMMENT_SINGLE."""
        code = "// comment"
        tokens = list(solidity_lexer.tokenize(code))
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT_SINGLE]
        assert len(comment_tokens) == 1

    def test_block_comment(self, solidity_lexer) -> None:
        """/* */ comments should be COMMENT_MULTILINE."""
        code = "/* block */"
        tokens = list(solidity_lexer.tokenize(code))
        comment_tokens = [t for t in tokens if t.type == TokenType.COMMENT_MULTILINE]
        assert len(comment_tokens) == 1

    def test_natspec_doc_comment(self, solidity_lexer) -> None:
        """/** */ NatSpec should be STRING_DOC."""
        code = "/** @param x The value */"
        tokens = list(solidity_lexer.tokenize(code))
        doc_tokens = [t for t in tokens if t.type == TokenType.STRING_DOC]
        assert len(doc_tokens) == 1


class TestSolidityOperators:
    """Test Solidity operator tokenization."""

    def test_function_type_arrow(self, solidity_lexer) -> None:
        """=> for function types should be OPERATOR."""
        code = "function() => uint"
        tokens = list(solidity_lexer.tokenize(code))
        arrow_tokens = [t for t in tokens if t.value == "=>"]
        assert len(arrow_tokens) == 1
        assert arrow_tokens[0].type == TokenType.OPERATOR


class TestSolidityStrings:
    """Test Solidity string tokenization."""

    def test_double_quoted_string(self, solidity_lexer) -> None:
        """Double-quoted strings should be STRING."""
        code = '"hello"'
        tokens = list(solidity_lexer.tokenize(code))
        string_tokens = [t for t in tokens if t.type == TokenType.STRING]
        assert len(string_tokens) == 1


class TestSolidityComplex:
    """Test complex Solidity code."""

    def test_contract_declaration(self, solidity_lexer) -> None:
        """Contract with method should tokenize correctly."""
        code = "contract Foo { function bar() public view returns (uint) { return 1; } }"
        tokens = list(solidity_lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.KEYWORD_DECLARATION in types
        assert TokenType.NAME_CLASS in types
        assert TokenType.KEYWORD_TYPE in types

    def test_mapping_declaration(self, solidity_lexer) -> None:
        """Mapping declaration should tokenize correctly."""
        code = "mapping(address => uint) public balances;"
        tokens = list(solidity_lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "mapping" in values
        assert "address" in values
        assert "uint" in values
        assert "=>" in values

    def test_fixture_basics(self, solidity_lexer) -> None:
        """Fixture basics.sol should tokenize without error."""
        from pathlib import Path

        fixture_path = Path(__file__).parent.parent / "fixtures" / "solidity" / "basics.sol"
        if not fixture_path.exists():
            pytest.skip("fixtures/solidity/basics.sol not found")
        code = fixture_path.read_text(encoding="utf-8")
        tokens = list(solidity_lexer.tokenize(code))
        assert len(tokens) > 0
        error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
        assert len(error_tokens) == 0
