"""Protocol definitions for Rosettes.

Defines the contracts that lexers and formatters must implement.
All implementations must be thread-safe.

Design Philosophy:
    Rosettes uses Protocol (structural typing) rather than abstract base classes.
    This enables:

    - **Duck typing with safety**: Any object with the right methods works
    - **No inheritance hierarchy**: Cleaner, more flexible implementations
    - **Easy testing**: Create minimal mock implementations without inheritance
    - **Gradual adoption**: Existing classes can satisfy protocols without changes

When to Implement:
    Lexer Protocol:
        ✅ Adding support for a new programming language
        ✅ Creating a specialized lexer (e.g., for a DSL)
        ✅ Wrapping an external tokenizer with Rosettes interface

    Formatter Protocol:
        ✅ New output format (LaTeX, RTF, Markdown, etc.)
        ✅ Custom HTML structure for specific frameworks
        ✅ Integration with external rendering systems

Example (Custom Lexer):
    >>> class MyDslLexer:
    ...     name = "mydsl"
    ...     aliases = ("dsl",)
    ...     filenames = ("*.dsl",)
    ...     mimetypes = ()
    ...
    ...     def tokenize(self, code, config=None, start=0, end=None):
    ...         # Your tokenization logic here
    ...         yield Token(TokenType.TEXT, code, 1, 1)
    ...
    ...     def tokenize_fast(self, code, start=0, end=None):
    ...         yield (TokenType.TEXT, code)

Example (Custom Formatter):
    >>> class MarkdownFormatter:
    ...     name = "markdown"
    ...
    ...     def format(self, tokens, config=None):
    ...         for token in tokens:
    ...             if token.type == TokenType.KEYWORD:
    ...                 yield f"**{token.value}**"
    ...             else:
    ...                 yield token.value

See Also:
    rosettes.lexers._state_machine: Base class for hand-written lexers
    rosettes.formatters.html: Reference Formatter implementation
    rosettes._registry: How lexers are registered and looked up
"""

from collections.abc import Iterator
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from ._config import FormatConfig, LexerConfig
from ._types import Token, TokenType

if TYPE_CHECKING:
    pass

__all__ = ["Lexer", "Formatter"]


@runtime_checkable
class Lexer(Protocol):
    """Protocol for tokenizers.

    Implementations must be thread-safe — no mutable shared state.
    The tokenize method should only use local variables.

    Thread-Safety Contract:
        - tokenize() must use only local variables
        - No instance state mutation during tokenization
        - Class-level constants (KEYWORDS, etc.) must be immutable (frozenset)

    Performance Contract:
        - O(n) time complexity guaranteed (no backtracking)
        - Single pass through input (no lookahead beyond current position)
        - Streaming output (yield tokens as found)

    See Also:
        rosettes.lexers._state_machine.StateMachineLexer: Base implementation
    """

    @property
    def name(self) -> str:
        """The canonical name of this lexer (e.g., 'python')."""
        ...

    @property
    def aliases(self) -> tuple[str, ...]:
        """Alternative names for this lexer (e.g., ('py', 'python3'))."""
        ...

    @property
    def filenames(self) -> tuple[str, ...]:
        """Glob patterns for files this lexer handles (e.g., ('*.py',))."""
        ...

    @property
    def mimetypes(self) -> tuple[str, ...]:
        """MIME types this lexer handles."""
        ...

    def tokenize(
        self,
        code: str,
        config: LexerConfig | None = None,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[Token]:
        """Tokenize source code into a stream of tokens.

        Args:
            code: The source code to tokenize.
            config: Optional lexer configuration.
            start: Starting index in the source string.
            end: Optional ending index in the source string.

        Yields:
            Token objects in order of appearance.
        """
        ...

    def tokenize_fast(
        self,
        code: str,
        start: int = 0,
        end: int | None = None,
    ) -> Iterator[tuple[TokenType, str]]:
        """Fast tokenization without position tracking.

        Yields minimal (type, value) tuples for maximum speed.
        Use when line/column info is not needed.

        Args:
            code: The source code to tokenize.
            start: Starting index in the source string.
            end: Optional ending index in the source string.

        Yields:
            (TokenType, value) tuples.
        """
        ...


@runtime_checkable
class Formatter(Protocol):
    """Protocol for output formatters.

    Implementations must be thread-safe — use only local variables in format().
    Formatter instances should be immutable (frozen dataclasses recommended).

    Thread-Safety Contract:
        - format() must use only local variables
        - Instance state must be immutable after construction
        - No side effects (file I/O, network, etc.)

    Streaming Contract:
        - format() yields chunks as they're ready (generator)
        - format_string() convenience method joins chunks
        - Callers can start processing before full output is ready

    Fast Path:
        - format_fast() accepts (TokenType, value) tuples instead of Token objects
        - Avoids Token construction overhead when position info not needed
        - ~20% faster for simple highlighting without line numbers

    See Also:
        rosettes.formatters.html.HtmlFormatter: Reference implementation
        rosettes.formatters.terminal.TerminalFormatter: ANSI terminal output
    """

    @property
    def name(self) -> str:
        """The canonical name of this formatter (e.g., 'html')."""
        ...

    def format(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Format tokens into output chunks.

        Args:
            tokens: Stream of tokens to format.
            config: Optional formatter configuration.

        Yields:
            String chunks of formatted output.
        """
        ...

    def format_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> Iterator[str]:
        """Fast formatting without position tracking.

        Args:
            tokens: Stream of (TokenType, value) tuples.
            config: Optional formatter configuration.

        Yields:
            String chunks of formatted output.
        """
        ...

    def format_string(
        self,
        tokens: Iterator[Token],
        config: FormatConfig | None = None,
    ) -> str:
        """Format tokens and return as a single string.

        Convenience method that joins format() output.

        Args:
            tokens: Stream of tokens to format.
            config: Optional formatter configuration.

        Returns:
            Complete formatted string.
        """
        ...

    def format_string_fast(
        self,
        tokens: Iterator[tuple[TokenType, str]],
        config: FormatConfig | None = None,
    ) -> str:
        """Fast format and return as a single string.

        Convenience method that joins format_fast() output.

        Args:
            tokens: Stream of (TokenType, value) tuples.
            config: Optional formatter configuration.

        Returns:
            Complete formatted string.
        """
        ...
