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
        code = """<?php
$text = <<<EOT
This is heredoc
text content
EOT;
?>"""
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

    def test_use_statement(self) -> None:
        lexer = get_lexer("php")
        code = "<?php use App\\Models\\User; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "use" in values

    def test_static_method_call(self) -> None:
        lexer = get_lexer("php")
        code = "<?php User::find(1); ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "::" in values

    def test_arrow_function(self) -> None:
        lexer = get_lexer("php")
        code = "<?php $fn = fn($x) => $x * 2; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "fn" in values or "=>" in values

    def test_match_expression(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
$result = match($x) {
    1 => 'one',
    2 => 'two',
    default => 'other',
};
?>"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "match" in values

    def test_null_safe_operator(self) -> None:
        lexer = get_lexer("php")
        code = "<?php $value = $user?->name; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "?->" in values or ("?" in values and "->" in values)

    def test_attribute(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
#[Route('/api')]
class Controller {}
?>"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        # PHP 8 attributes may be tokenized as single token or as comment-like
        assert any("#[" in v or "Route" in v for v in values)

    def test_interface(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
interface Countable {
    public function count(): int;
}
?>"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "interface" in values

    def test_trait(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
trait Loggable {
    public function log($msg) {}
}
?>"""
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "trait" in values

    def test_typed_properties(self) -> None:
        lexer = get_lexer("php")
        code = "<?php public int $count = 0; ?>"
        tokens = list(lexer.tokenize(code))
        values = [t.value for t in tokens]
        assert "int" in values

    def test_numeric_literals(self) -> None:
        lexer = get_lexer("php")
        code = """<?php
$int = 42;
$float = 3.14;
$hex = 0xFF;
$binary = 0b1010;
?>"""
        tokens = list(lexer.tokenize(code))
        types = [t.type for t in tokens]
        assert TokenType.NUMBER in types or TokenType.NUMBER_INTEGER in types

