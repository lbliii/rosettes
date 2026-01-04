"""Rosettes formatters package.

Contains output formatters for different targets (HTML, terminal, etc.).
"""

from rosettes.formatters.html import HtmlFormatter
from rosettes.formatters.null import NullFormatter
from rosettes.formatters.terminal import TerminalFormatter

__all__ = ["HtmlFormatter", "TerminalFormatter", "NullFormatter"]
