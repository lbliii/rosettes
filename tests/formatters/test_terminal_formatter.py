from rosettes import highlight
from rosettes.formatters.terminal import TerminalFormatter

def test_terminal_highlight():
    code = "def foo(): pass"
    output = highlight(code, "python", formatter="terminal")
    
    # Check for ANSI escape codes
    assert "\033[" in output
    assert "\033[0m" in output  # Reset code
    
    # Check for specific colors
    # def = DECLARATION = \033[36m
    # pass = CONTROL_FLOW = \033[35m
    assert "\033[36mdef\033[0m" in output
    assert "\033[35mpass\033[0m" in output

def test_terminal_formatter_direct():
    from rosettes import get_lexer
    lexer = get_lexer("python")
    tokens = lexer.tokenize("x = 1")
    formatter = TerminalFormatter()
    output = formatter.format_string(tokens)
    
    # x = VARIABLE (\033[37m)
    # = = OPERATOR (\033[37m)
    # 1 = NUMBER (\033[33m)
    assert "\033[37mx\033[0m" in output
    assert "\033[37m=\033[0m" in output
    assert "\033[33m1\033[0m" in output

def test_terminal_highlight_many():
    from rosettes import highlight_many
    blocks = [
        ("x = 1", "python"),
        ("let y = 2;", "javascript"),
    ]
    results = highlight_many(blocks, formatter="terminal")
    
    assert len(results) == 2
    assert "\033[" in results[0]
    assert "\033[" in results[1]

