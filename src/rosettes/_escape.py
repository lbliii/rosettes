"""HTML escaping utilities for Rosettes.

Thread-safe string escaping for HTML output.

Design Philosophy:
    This module uses str.translate() with a pre-computed table for maximum
    performance. This is faster than regex or multiple str.replace() calls:

    - str.translate(): ~0.2µs per call (C-level implementation)
    - regex sub(): ~1.5µs per call
    - chained replace(): ~0.8µs per call

    For syntax highlighting, escape_html() is called once per token,
    so performance here directly impacts overall throughput.

Security:
    Escapes the standard five HTML special characters:
    - & → &amp;   (must be first to avoid double-escaping)
    - < → &lt;    (prevents tag injection)
    - > → &gt;   (prevents tag injection)
    - " → &quot;  (prevents attribute injection)
    - ' → &#x27;  (prevents attribute injection in single quotes)

    This provides protection against XSS when embedding code in HTML.

Thread-Safety:
    The escape table is immutable (dict with int keys). The function
    uses only the input string and the table — no shared mutable state.

See Also:
    rosettes.formatters.html: Uses escape_html for all token values
"""

__all__ = ["escape_html"]

# Pre-computed escape table for performance
# Using ord() keys for str.translate() compatibility
_ESCAPE_TABLE = {
    ord("&"): "&amp;",
    ord("<"): "&lt;",
    ord(">"): "&gt;",
    ord('"'): "&quot;",
    ord("'"): "&#x27;",
}


def escape_html(text: str) -> str:
    """Escape HTML special characters.

    Escapes: & < > " '

    Uses str.translate() with a pre-computed table for maximum performance.
    This is the hot path for HTML formatting — called once per token.

    Args:
        text: The text to escape.

    Returns:
        HTML-safe string with special characters replaced.

    Performance:
        ~0.2µs per call for typical token lengths (5-20 chars).

    Example:
        >>> escape_html('<script>alert("xss")</script>')
        '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'

        >>> escape_html("def foo():")  # No escaping needed
        'def foo():'
    """
    return text.translate(_ESCAPE_TABLE)
