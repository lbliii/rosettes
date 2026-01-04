"""Lazy lexer registry for Rosettes.

All lexers are hand-written state machines with O(n) guaranteed performance
and zero ReDoS vulnerability. Lexers are loaded on-demand using functools.cache
for thread-safe memoization.

Design Philosophy:
    The registry uses lazy loading with caching to balance startup time and
    runtime performance:

    1. **Zero startup cost**: No lexers imported at module load time
    2. **O(1) lookup**: Pre-computed alias table for instant name resolution
    3. **Single instance**: functools.cache ensures one lexer per language
    4. **Thread-safe**: cache is thread-safe; lexers are stateless

Architecture:
    _LEXER_SPECS: Static registry mapping names to (module, class) specs
    _ALIAS_TO_NAME: Pre-computed case-insensitive alias lookup table
    _get_lexer_by_canonical: Cached lexer instantiation (one per language)

Performance Notes:
    - First call: ~1ms (module import + class instantiation)
    - Subsequent calls: ~100ns (dict lookup + cache hit)
    - Memory: ~500 bytes per loaded lexer

Common Mistakes:
    # ❌ WRONG: Caching lexer instances yourself
    lexer_cache = {}
    if lang not in lexer_cache:
        lexer_cache[lang] = get_lexer(lang)

    # ✅ CORRECT: Just call get_lexer() — it's already cached
    lexer = get_lexer(lang)

    # ❌ WRONG: Checking support by catching exceptions
    try:
        lexer = get_lexer(lang)
    except LookupError:
        lexer = None

    # ✅ CORRECT: Use supports_language() for checks
    if supports_language(lang):
        lexer = get_lexer(lang)

Adding New Languages:
    To add a new language, create a lexer in rosettes/lexers/ and add an
    entry to _LEXER_SPECS below. See rosettes/lexers/_state_machine.py for
    the base class and helper functions.

See Also:
    rosettes.lexers._state_machine: Base class for lexer implementations
    rosettes._protocol.Lexer: Protocol that all lexers must satisfy
    rosettes._formatter_registry: Similar pattern for formatters
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lexers._state_machine import StateMachineLexer

__all__ = ["get_lexer", "list_languages", "supports_language"]


@dataclass(frozen=True, slots=True)
class LexerSpec:
    """Specification for lazy-loading a lexer.

    Used internally by the registry to defer module imports until first use.
    This keeps `import rosettes` fast (~5ms) even with 50+ language support.

    Attributes:
        module: Full module path (e.g., 'rosettes.lexers.python_sm').
        class_name: Name of the lexer class in the module.
        aliases: Alternative names for lookup (e.g., 'py' for 'python').

    Example:
        >>> spec = LexerSpec(
        ...     "rosettes.lexers.python_sm",
        ...     "PythonStateMachineLexer",
        ...     aliases=("py", "python3"),
        ... )

    Note:
        Aliases are case-insensitive. Both 'Python' and 'PYTHON' resolve
        to the canonical name 'python'.
    """

    module: str
    class_name: str
    aliases: tuple[str, ...] = ()


# Static registry — all state machine lexers (O(n) guaranteed, zero ReDoS)
_LEXER_SPECS: dict[str, LexerSpec] = {
    # Core languages
    "python": LexerSpec(
        "rosettes.lexers.python_sm",
        "PythonStateMachineLexer",
        aliases=("py", "python3", "py3"),
    ),
    "javascript": LexerSpec(
        "rosettes.lexers.javascript_sm",
        "JavaScriptStateMachineLexer",
        aliases=("js", "ecmascript", "jsx"),
    ),
    "typescript": LexerSpec(
        "rosettes.lexers.typescript_sm",
        "TypeScriptStateMachineLexer",
        aliases=("ts",),
    ),
    "json": LexerSpec(
        "rosettes.lexers.json_sm",
        "JsonStateMachineLexer",
        aliases=("json5",),
    ),
    "yaml": LexerSpec(
        "rosettes.lexers.yaml_sm",
        "YamlStateMachineLexer",
        aliases=("yml",),
    ),
    "toml": LexerSpec(
        "rosettes.lexers.toml_sm",
        "TomlStateMachineLexer",
        aliases=(),
    ),
    "bash": LexerSpec(
        "rosettes.lexers.bash_sm",
        "BashStateMachineLexer",
        aliases=("sh", "shell", "zsh", "ksh"),
    ),
    "html": LexerSpec(
        "rosettes.lexers.html_sm",
        "HtmlStateMachineLexer",
        aliases=("htm", "xhtml", "go-html-template"),
    ),
    "css": LexerSpec(
        "rosettes.lexers.css_sm",
        "CssStateMachineLexer",
        aliases=(),
    ),
    "diff": LexerSpec(
        "rosettes.lexers.diff_sm",
        "DiffStateMachineLexer",
        aliases=("patch", "udiff"),
    ),
    # Systems languages
    "c": LexerSpec(
        "rosettes.lexers.c_sm",
        "CStateMachineLexer",
        aliases=("h",),
    ),
    "cpp": LexerSpec(
        "rosettes.lexers.cpp_sm",
        "CppStateMachineLexer",
        aliases=("c++", "cxx", "hpp"),
    ),
    "rust": LexerSpec(
        "rosettes.lexers.rust_sm",
        "RustStateMachineLexer",
        aliases=("rs",),
    ),
    "go": LexerSpec(
        "rosettes.lexers.go_sm",
        "GoStateMachineLexer",
        aliases=("golang",),
    ),
    "zig": LexerSpec(
        "rosettes.lexers.zig_sm",
        "ZigStateMachineLexer",
        aliases=(),
    ),
    # JVM languages
    "java": LexerSpec(
        "rosettes.lexers.java_sm",
        "JavaStateMachineLexer",
        aliases=(),
    ),
    "kotlin": LexerSpec(
        "rosettes.lexers.kotlin_sm",
        "KotlinStateMachineLexer",
        aliases=("kt", "kts"),
    ),
    "scala": LexerSpec(
        "rosettes.lexers.scala_sm",
        "ScalaStateMachineLexer",
        aliases=("sc",),
    ),
    "groovy": LexerSpec(
        "rosettes.lexers.groovy_sm",
        "GroovyStateMachineLexer",
        aliases=("gradle", "gvy"),
    ),
    "clojure": LexerSpec(
        "rosettes.lexers.clojure_sm",
        "ClojureStateMachineLexer",
        aliases=("clj", "edn"),
    ),
    # Apple ecosystem
    "swift": LexerSpec(
        "rosettes.lexers.swift_sm",
        "SwiftStateMachineLexer",
        aliases=(),
    ),
    # Scripting languages
    "ruby": LexerSpec(
        "rosettes.lexers.ruby_sm",
        "RubyStateMachineLexer",
        aliases=("rb",),
    ),
    "perl": LexerSpec(
        "rosettes.lexers.perl_sm",
        "PerlStateMachineLexer",
        aliases=("pl", "pm"),
    ),
    "php": LexerSpec(
        "rosettes.lexers.php_sm",
        "PhpStateMachineLexer",
        aliases=("php3", "php4", "php5", "php7", "php8"),
    ),
    "lua": LexerSpec(
        "rosettes.lexers.lua_sm",
        "LuaStateMachineLexer",
        aliases=(),
    ),
    "r": LexerSpec(
        "rosettes.lexers.r_sm",
        "RStateMachineLexer",
        aliases=("rlang", "splus"),
    ),
    "powershell": LexerSpec(
        "rosettes.lexers.powershell_sm",
        "PowershellStateMachineLexer",
        aliases=("posh", "ps1", "psm1", "pwsh"),
    ),
    # Functional languages
    "haskell": LexerSpec(
        "rosettes.lexers.haskell_sm",
        "HaskellStateMachineLexer",
        aliases=("hs",),
    ),
    "elixir": LexerSpec(
        "rosettes.lexers.elixir_sm",
        "ElixirStateMachineLexer",
        aliases=("ex", "exs"),
    ),
    # Data/query languages
    "sql": LexerSpec(
        "rosettes.lexers.sql_sm",
        "SqlStateMachineLexer",
        aliases=("mysql", "postgresql", "sqlite"),
    ),
    "csv": LexerSpec(
        "rosettes.lexers.csv_sm",
        "CsvStateMachineLexer",
        aliases=("tsv",),
    ),
    "graphql": LexerSpec(
        "rosettes.lexers.graphql_sm",
        "GraphqlStateMachineLexer",
        aliases=("gql",),
    ),
    # Markup
    "markdown": LexerSpec(
        "rosettes.lexers.markdown_sm",
        "MarkdownStateMachineLexer",
        aliases=("md", "mdown"),
    ),
    "xml": LexerSpec(
        "rosettes.lexers.xml_sm",
        "XmlStateMachineLexer",
        aliases=("xsl", "xslt", "rss", "svg"),
    ),
    # Config formats
    "ini": LexerSpec(
        "rosettes.lexers.ini_sm",
        "IniStateMachineLexer",
        aliases=("cfg", "dosini", "properties", "conf", "apache"),
    ),
    "nginx": LexerSpec(
        "rosettes.lexers.nginx_sm",
        "NginxStateMachineLexer",
        aliases=("nginxconf",),
    ),
    "dockerfile": LexerSpec(
        "rosettes.lexers.dockerfile_sm",
        "DockerfileStateMachineLexer",
        aliases=("docker",),
    ),
    "makefile": LexerSpec(
        "rosettes.lexers.makefile_sm",
        "MakefileStateMachineLexer",
        aliases=("make", "mf", "bsdmake"),
    ),
    "hcl": LexerSpec(
        "rosettes.lexers.hcl_sm",
        "HclStateMachineLexer",
        aliases=("terraform", "tf"),
    ),
    # Schema/IDL
    "protobuf": LexerSpec(
        "rosettes.lexers.protobuf_sm",
        "ProtobufStateMachineLexer",
        aliases=("proto", "proto3"),
    ),
    # Modern/emerging languages
    "dart": LexerSpec(
        "rosettes.lexers.dart_sm",
        "DartStateMachineLexer",
        aliases=(),
    ),
    "julia": LexerSpec(
        "rosettes.lexers.julia_sm",
        "JuliaStateMachineLexer",
        aliases=("jl",),
    ),
    "nim": LexerSpec(
        "rosettes.lexers.nim_sm",
        "NimStateMachineLexer",
        aliases=("nimrod",),
    ),
    "gleam": LexerSpec(
        "rosettes.lexers.gleam_sm",
        "GleamStateMachineLexer",
        aliases=(),
    ),
    "v": LexerSpec(
        "rosettes.lexers.v_sm",
        "VStateMachineLexer",
        aliases=("vlang",),
    ),
    # AI/ML specialized
    "mojo": LexerSpec(
        "rosettes.lexers.mojo_sm",
        "MojoStateMachineLexer",
        aliases=("🔥",),
    ),
    "triton": LexerSpec(
        "rosettes.lexers.triton_sm",
        "TritonStateMachineLexer",
        aliases=(),
    ),
    "cuda": LexerSpec(
        "rosettes.lexers.cuda_sm",
        "CudaStateMachineLexer",
        aliases=("cu",),
    ),
    "stan": LexerSpec(
        "rosettes.lexers.stan_sm",
        "StanStateMachineLexer",
        aliases=(),
    ),
    # Configuration languages
    "pkl": LexerSpec(
        "rosettes.lexers.pkl_sm",
        "PklStateMachineLexer",
        aliases=(),
    ),
    "cue": LexerSpec(
        "rosettes.lexers.cue_sm",
        "CueStateMachineLexer",
        aliases=(),
    ),
    # Tree/directory
    "tree": LexerSpec(
        "rosettes.lexers.tree_sm",
        "TreeStateMachineLexer",
        aliases=("directory", "filetree", "dirtree", "files", "scm", "treesitter"),
    ),
    # Template languages
    "kida": LexerSpec(
        "rosettes.lexers.kida_sm",
        "KidaStateMachineLexer",
        aliases=("bengal-template",),
    ),
    "jinja": LexerSpec(
        "rosettes.lexers.jinja_sm",
        "JinjaStateMachineLexer",
        aliases=("jinja2", "j2", "django"),
    ),
    # Plaintext (no highlighting)
    "plaintext": LexerSpec(
        "rosettes.lexers.plaintext_sm",
        "PlaintextStateMachineLexer",
        aliases=("text", "plain", "txt", "none", "raw", "rst"),
    ),
}

# Build alias lookup table (case-insensitive)
_ALIAS_TO_NAME: dict[str, str] = {}
for _name, _spec in _LEXER_SPECS.items():
    _ALIAS_TO_NAME[_name] = _name
    _ALIAS_TO_NAME[_name.upper()] = _name  # Pre-compute uppercase
    for _alias in _spec.aliases:
        _ALIAS_TO_NAME[_alias] = _name
        _ALIAS_TO_NAME[_alias.upper()] = _name

# Pre-compute sorted language list (avoid sorting on each call)
_SORTED_LANGUAGES: list[str] = sorted(_LEXER_SPECS.keys())


def _normalize_name(name: str) -> str:
    """Normalize a language name to its canonical form. O(1) lookup.

    Args:
        name: Language name or alias.

    Returns:
        Canonical language name.

    Raises:
        LookupError: If the language is not supported.
    """
    # Try direct lookup first (common case: already lowercase)
    if name in _ALIAS_TO_NAME:
        return _ALIAS_TO_NAME[name]
    # Try lowercase (avoid strip - rarely needed)
    lower = name.lower()
    if lower in _ALIAS_TO_NAME:
        return _ALIAS_TO_NAME[lower]

    raise LookupError(f"Unknown language: {name!r}. Supported: {_SORTED_LANGUAGES}")


def get_lexer(name: str) -> StateMachineLexer:
    """Get a lexer instance by name or alias.

    All lexers are hand-written state machines with O(n) guaranteed
    performance and zero ReDoS vulnerability.

    Uses functools.cache for thread-safe memoization.
    Lexers are loaded lazily on first access.

    Args:
        name: Language name or alias (e.g., 'python', 'py', 'js').

    Returns:
        StateMachineLexer instance.

    Raises:
        LookupError: If the language is not supported.

    Example:
        >>> lexer = get_lexer("python")
        >>> lexer.name
        'python'
        >>> get_lexer("py") is lexer  # Same instance (cached)
        True
    """
    canonical = _normalize_name(name)
    return _get_lexer_by_canonical(canonical)


@cache
def _get_lexer_by_canonical(canonical: str) -> StateMachineLexer:
    """Internal cached loader - keyed by canonical name."""
    spec = _LEXER_SPECS[canonical]
    module = import_module(spec.module)
    lexer_class = getattr(module, spec.class_name)
    return lexer_class()


def list_languages() -> list[str]:
    """List all supported language names. O(1).

    Returns:
        Sorted list of canonical language names.
    """
    return _SORTED_LANGUAGES.copy()  # Return copy to prevent mutation


def supports_language(name: str) -> bool:
    """Check if a language is supported.

    Args:
        name: Language name or alias.

    Returns:
        True if the language is supported.
    """
    # Fast path: direct lookup without triggering error import
    if name in _ALIAS_TO_NAME:
        return True
    lower = name.lower()
    return lower in _ALIAS_TO_NAME
