"""Rosettes formatters package.

Contains output formatters for different targets (HTML, terminal, etc.).

Available Formatters:
    HtmlFormatter: HTML output with semantic or Pygments-compatible CSS classes
    TerminalFormatter: ANSI escape codes for terminal output
    NullFormatter: No-op formatter for testing and benchmarking

Usage:
    Most users should use the high-level rosettes.highlight() function
    with the `formatter` parameter:

        >>> from rosettes import highlight
        >>> html = highlight("def foo(): pass", "python", formatter="html")
        >>> ansi = highlight("def foo(): pass", "python", formatter="terminal")

    Direct formatter usage is for:
        - Custom processing pipelines
        - Streaming output to files
        - Integration with external systems

Custom Formatters:
    To create a custom formatter, implement the rosettes._protocol.Formatter
    protocol. See rosettes.formatters.html for a reference implementation.

See Also:
    rosettes._protocol.Formatter: Protocol definition for formatters
    rosettes._formatter_registry: How formatters are registered
"""

from rosettes.formatters.html import HtmlFormatter
from rosettes.formatters.null import NullFormatter
from rosettes.formatters.terminal import TerminalFormatter

__all__ = ["HtmlFormatter", "TerminalFormatter", "NullFormatter"]
