#!/usr/bin/env python3
"""Generate golden fixtures for lexer tests.

Usage:
    uv run python scripts/generate_fixtures.py --all
    uv run python scripts/generate_fixtures.py --language python
    uv run python scripts/generate_fixtures.py --update  # Regenerate existing
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rosettes import get_lexer, list_languages

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures"

# Sample code for each language (representative constructs)
LANGUAGE_SAMPLES: dict[str, dict[str, str]] = {
    "python": {
        "keywords": '''if True:
    pass
elif False:
    pass
else:
    pass

for x in range(10):
    continue
    break

def func():
    return None

class MyClass:
    pass

try:
    raise Exception
except Exception:
    pass

import os
from sys import path

async def async_func():
    await something()
''',
        "strings": '''x = "hello"
y = 'world'
z = """multiline
string"""
f = f"interpolated {value}"
r = r"raw\\string"
''',
        "numbers": '''a = 42
b = 3.14
c = 1e-10
d = 0xFF
e = 0b1010
f = 1_000_000
''',
        "comments": '''# This is a single line comment
x = 1  # inline comment

"""
This is a docstring
spanning multiple lines
"""

def foo():
    """Function docstring."""
    pass
''',
        "operators": '''# Arithmetic
a = 1 + 2
b = 3 - 4
c = 5 * 6
d = 7 / 8
e = 9 // 10
f = 11 % 12
g = 2 ** 3

# Comparison
x = a == b
y = a != b
z = a < b
w = a > b
p = a <= b
q = a >= b

# Logical
r = True and False
s = True or False
t = not True

# Bitwise
u = a & b
v = a | b
''',
        "decorators": '''@property
def value(self):
    return self._value

@staticmethod
def static_method():
    pass

@classmethod
def class_method(cls):
    pass

@decorator_with_args(x=1, y=2)
def decorated():
    pass

@functools.lru_cache(maxsize=128)
def cached_func():
    pass
''',
        "type_annotations": '''from typing import List, Dict, Optional, Union

def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: List[int]) -> Dict[str, int]:
    return {"count": len(items)}

x: int = 42
y: Optional[str] = None
z: Union[int, str] = "hello"

class User:
    name: str
    age: int
''',
    },
    "javascript": {
        "keywords": '''if (true) {
    const x = 1;
    let y = 2;
    var z = 3;
}

for (const item of items) {
    continue;
    break;
}

function greet(name) {
    return `Hello ${name}`;
}

class MyClass extends Base {
    constructor() {
        super();
    }
}

async function fetchData() {
    await fetch(url);
}

import { x } from "module";
export default MyClass;
''',
        "strings": '''const single = 'hello';
const double = "world";
const template = `hello ${name}`;
const multiline = `line 1
line 2`;
''',
        "numbers": '''const int = 42;
const float = 3.14;
const hex = 0xFF;
const binary = 0b1010;
const bigint = 100n;
''',
        "comments": '''// Single line comment
const x = 1; // inline comment

/* 
 * Multi-line comment
 * spanning multiple lines
 */

/**
 * JSDoc comment
 * @param {string} name - The name
 * @returns {string} Greeting
 */
function greet(name) {
    return `Hello, ${name}`;
}
''',
        "operators": '''// Arithmetic
const a = 1 + 2;
const b = 3 - 4;
const c = 5 * 6;
const d = 7 / 8;
const e = 9 % 10;
const f = 2 ** 3;

// Comparison
const eq = a === b;
const neq = a !== b;
const lt = a < b;
const gt = a > b;

// Logical
const and = true && false;
const or = true || false;
const not = !true;
const nullish = a ?? b;

// Optional chaining
const prop = obj?.property;
''',
        "arrow_functions": '''const simple = x => x + 1;

const withParams = (a, b) => a + b;

const withBody = (x) => {
    const y = x * 2;
    return y + 1;
};

const asyncArrow = async (url) => {
    const response = await fetch(url);
    return response.json();
};

const array = [1, 2, 3].map(x => x * 2);
''',
    },
    "typescript": {
        "types": '''interface User {
    name: string;
    age: number;
}

type Status = "active" | "inactive";

function greet(user: User): string {
    return `Hello ${user.name}`;
}

const numbers: number[] = [1, 2, 3];
const map: Map<string, number> = new Map();

class Service<T> {
    data: T;
}
''',
    },
    "rust": {
        "keywords": '''fn main() {
    let x = 42;
    let mut y = 0;
    
    if x > 0 {
        println!("positive");
    } else {
        println!("non-positive");
    }
    
    for i in 0..10 {
        continue;
    }
    
    loop {
        break;
    }
    
    match x {
        0 => println!("zero"),
        _ => println!("other"),
    }
}

struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
}

trait Drawable {
    fn draw(&self);
}

async fn async_fn() {
    do_something().await;
}
''',
        "types": '''let x: i32 = 42;
let y: f64 = 3.14;
let s: &str = "hello";
let v: Vec<i32> = vec![1, 2, 3];
let opt: Option<i32> = Some(42);
let res: Result<i32, String> = Ok(42);
''',
        "strings": '''let single = "hello world";
let raw = r#"raw string with "quotes""#;
let byte = b"byte string";
let multiline = "line 1
line 2";
let with_escapes = "tab:\\t newline:\\n";
let char_literal = 'a';
''',
        "numbers": '''let integer = 42;
let negative = -17;
let float = 3.14;
let scientific = 1e10;
let hex = 0xFF;
let octal = 0o755;
let binary = 0b1010;
let underscore = 1_000_000;
let typed = 42i64;
let float_typed = 3.14f32;
''',
        "comments": '''// Single line comment
let x = 1; // inline comment

/* 
 * Multi-line comment
 */

/// Documentation comment for function
/// 
/// # Examples
/// 
/// ```
/// let x = example();
/// ```
fn example() -> i32 {
    42
}

//! Module-level documentation
''',
        "operators": '''// Arithmetic
let a = 1 + 2;
let b = 3 - 4;
let c = 5 * 6;
let d = 7 / 8;
let e = 9 % 10;

// Comparison
let eq = a == b;
let neq = a != b;
let lt = a < b;
let gt = a > b;

// Logical
let and = true && false;
let or = true || false;
let not = !true;

// Bitwise
let band = a & b;
let bor = a | b;
let xor = a ^ b;

// Reference
let r = &x;
let m = &mut y;
''',
        "lifetimes": '''fn first<'a>(s: &'a str) -> &'a str {
    &s[0..1]
}

struct Wrapper<'a> {
    data: &'a str,
}

impl<'a> Wrapper<'a> {
    fn get(&self) -> &'a str {
        self.data
    }
}

fn longest<'a, 'b: 'a>(x: &'a str, y: &'b str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

static STATIC_STR: &'static str = "hello";
''',
    },
    "kida": {
        "expressions": '''{{ variable }}
{{ user.name }}
{{ items[0] }}
{{ value | upper }}
{{ value | slugify | trim }}
{{ "Hello, " ~ name ~ "!" }}
{{ count + 1 }}
{{ price * quantity }}
''',
        "statements": '''{% if condition %}
    Content when true
{% else %}
    Content when false
{% end %}

{% for item in items %}
    {{ item }}
{% end %}

{% set x = 1 %}

{% include "partial.html" %}

{% block content %}
    Default content
{% end %}

{% extends "base.html" %}
''',
        "pipeline": '''{{ value |> upper }}
{{ value |> trim |> slugify }}
{{ items |> first |> upper }}
{{ text |> split(",") |> join(" - ") }}
{{ data |> json_encode }}
''',
        "pattern_matching": '''{% match status %}
{% case "active" %}
    Active user
{% case "pending" %}
    Waiting for approval
{% case "inactive" %}
    Deactivated
{% default %}
    Unknown status
{% end %}
''',
        "builtins": '''{{ x | upper }}
{{ x | lower }}
{{ x | trim }}
{{ x | slugify }}
{{ items | first }}
{{ items | last }}
{{ items | length }}
{{ items | reverse }}
{{ items | sort }}
{{ value | default("N/A") }}
{% if x is defined %}defined{% end %}
{% if x is empty %}empty{% end %}
{% if x is iterable %}iterable{% end %}
''',
    },
    "yaml": {
        "basics": '''# Configuration file
name: my-app
version: 1.0.0

settings:
  debug: true
  port: 8080
  timeout: 30.5

database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret

features:
  - authentication
  - logging
  - caching

defaults: &defaults
  adapter: postgres
  pool: 5

production:
  <<: *defaults
  pool: 25
''',
    },
    "json": {
        "basics": '''{
    "name": "my-app",
    "version": "1.0.0",
    "enabled": true,
    "count": 42,
    "ratio": 3.14,
    "data": null,
    "items": [1, 2, 3],
    "nested": {
        "key": "value"
    }
}
''',
    },
    "php": {
        "basics": '''<?php
namespace App\\Models;

use App\\Traits\\Loggable;

class User {
    public string $name;
    private int $age;
    
    public function __construct(string $name, int $age) {
        $this->name = $name;
        $this->age = $age;
    }
    
    public function greet(): string {
        return "Hello, {$this->name}!";
    }
}

$user = new User("John", 30);
echo $user->greet();

// Arrow function
$double = fn($x) => $x * 2;

// Match expression
$result = match($status) {
    "active" => 1,
    "inactive" => 0,
    default => -1,
};
?>
''',
    },
    "go": {
        "basics": '''package main

import (
    "fmt"
    "net/http"
)

type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func (u *User) Greet() string {
    return fmt.Sprintf("Hello, %s!", u.Name)
}

func main() {
    user := &User{Name: "John", Age: 30}
    fmt.Println(user.Greet())
    
    for i := 0; i < 10; i++ {
        fmt.Println(i)
    }
    
    switch user.Age {
    case 0:
        fmt.Println("newborn")
    default:
        fmt.Println("older")
    }
}
''',
    },
    "bash": {
        "basics": '''#!/bin/bash

# Variables
NAME="world"
COUNT=10

# Function
greet() {
    echo "Hello, $1!"
}

# Conditionals
if [ "$NAME" = "world" ]; then
    echo "Hello World"
elif [ -z "$NAME" ]; then
    echo "No name"
else
    echo "Hello $NAME"
fi

# Loops
for i in $(seq 1 $COUNT); do
    echo "Iteration $i"
done

while true; do
    break
done

# Arrays
arr=(one two three)
echo "${arr[0]}"

# Command substitution
TODAY=$(date +%Y-%m-%d)
''',
    },
    "sql": {
        "basics": '''-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert data
INSERT INTO users (name, email)
VALUES ('John Doe', 'john@example.com');

-- Select with join
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 10;

-- Update
UPDATE users
SET name = 'Jane Doe'
WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
''',
    },
    "toml": {
        "basics": '''# Project configuration
[project]
name = "my-app"
version = "1.0.0"
description = "A sample application"
authors = ["Developer <dev@example.com>"]

[project.dependencies]
requests = "^2.28.0"
pydantic = { version = "^2.0", extras = ["email"] }

[tool.ruff]
line-length = 100
target-version = "py312"

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true
''',
    },
    "xml": {
        "basics": '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<root xmlns:custom="http://example.com/ns">
    <!-- Comment -->
    <element attribute="value">
        Text content
    </element>
    <self-closing />
    <custom:element>
        Namespaced content
    </custom:element>
    <![CDATA[
        Raw content here
    ]]>
</root>
''',
    },
    "html": {
        "basics": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sample Page</title>
    <style>
        body { margin: 0; }
    </style>
</head>
<body>
    <header id="main-header" class="container">
        <h1>Welcome</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/about">About</a>
        </nav>
    </header>
    <main>
        <p>Hello, <strong>World</strong>!</p>
        <img src="image.jpg" alt="Sample" />
    </main>
    <script>
        console.log("Hello");
    </script>
</body>
</html>
''',
    },
    "css": {
        "basics": '''/* Base styles */
:root {
    --primary: #3498db;
    --spacing: 16px;
}

body {
    margin: 0;
    padding: var(--spacing);
    font-family: system-ui, sans-serif;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

#header {
    background: linear-gradient(to right, #fff, #eee);
    border: 1px solid #ddd;
}

@media (max-width: 768px) {
    .container {
        padding: 8px;
    }
}

.button:hover {
    transform: scale(1.05);
    transition: transform 0.2s ease;
}
''',
    },
    "markdown": {
        "basics": '''# Heading 1

## Heading 2

Regular paragraph with **bold** and *italic* text.

- List item 1
- List item 2
  - Nested item

1. Numbered item
2. Another item

> Blockquote text

`inline code`

```python
def hello():
    print("Hello")
```

[Link text](https://example.com)

![Alt text](image.jpg)
''',
    },
}

# Extension mapping
EXTENSIONS: dict[str, str] = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
    "rust": ".rs",
    "go": ".go",
    "yaml": ".yaml",
    "json": ".json",
    "php": ".php",
    "bash": ".sh",
    "sql": ".sql",
    "toml": ".toml",
    "xml": ".xml",
    "html": ".html",
    "css": ".css",
    "markdown": ".md",
    "c": ".c",
    "cpp": ".cpp",
    "java": ".java",
    "kotlin": ".kt",
    "swift": ".swift",
    "ruby": ".rb",
    "perl": ".pl",
    "lua": ".lua",
    "r": ".r",
    "scala": ".scala",
    "haskell": ".hs",
    "elixir": ".ex",
    "clojure": ".clj",
    "julia": ".jl",
    "dart": ".dart",
    "nim": ".nim",
    "zig": ".zig",
    "v": ".v",
    "mojo": ".mojo",
    "kida": ".kida",
}


def get_extension(language: str) -> str:
    """Get file extension for language."""
    return EXTENSIONS.get(language, ".txt")


def generate_fixture(language: str, name: str, code: str) -> None:
    """Generate fixture files for a test case."""
    lang_dir = FIXTURES_DIR / language
    lang_dir.mkdir(parents=True, exist_ok=True)

    # Write source file
    ext = get_extension(language)
    source_file = lang_dir / f"{name}{ext}"
    source_file.write_text(code, encoding="utf-8")

    # Generate and write tokens
    lexer = get_lexer(language)
    tokens = [
        {"type": t.type.name, "value": t.value, "line": t.line, "column": t.column}
        for t in lexer.tokenize(code)
    ]
    tokens_file = lang_dir / f"{name}.tokens.json"
    tokens_file.write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Generated: {source_file.relative_to(FIXTURES_DIR.parent)}")


def generate_all() -> None:
    """Generate fixtures for all languages with samples."""
    for lang, samples in LANGUAGE_SAMPLES.items():
        for name, code in samples.items():
            generate_fixture(lang, name, code)


def generate_language(language: str) -> None:
    """Generate fixtures for a specific language."""
    samples = LANGUAGE_SAMPLES.get(language)
    if not samples:
        print(f"No samples defined for {language}")
        print(f"Available: {', '.join(sorted(LANGUAGE_SAMPLES.keys()))}")
        return

    for name, code in samples.items():
        generate_fixture(language, name, code)


def update_existing() -> None:
    """Regenerate tokens for existing fixture source files."""
    if not FIXTURES_DIR.exists():
        print("No fixtures directory found")
        return

    for lang_dir in FIXTURES_DIR.iterdir():
        if not lang_dir.is_dir():
            continue

        language = lang_dir.name
        if language not in list_languages():
            print(f"Skipping unknown language: {language}")
            continue

        lexer = get_lexer(language)

        for source_file in lang_dir.iterdir():
            # Skip token files and non-source files
            if source_file.suffix == ".json" or source_file.name.startswith("."):
                continue

            name = source_file.stem
            code = source_file.read_text(encoding="utf-8")

            tokens = [
                {"type": t.type.name, "value": t.value, "line": t.line, "column": t.column}
                for t in lexer.tokenize(code)
            ]
            tokens_file = lang_dir / f"{name}.tokens.json"
            tokens_file.write_text(
                json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8"
            )

            print(f"Updated: {tokens_file.relative_to(FIXTURES_DIR.parent)}")


def list_available() -> None:
    """List available languages and samples."""
    print("Languages with sample fixtures:")
    for lang in sorted(LANGUAGE_SAMPLES.keys()):
        samples = LANGUAGE_SAMPLES[lang]
        print(f"  {lang}: {', '.join(samples.keys())}")

    print("\nAll supported languages:")
    print(f"  {', '.join(sorted(list_languages()))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lexer test fixtures")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Generate all fixtures")
    group.add_argument("--language", type=str, help="Generate fixtures for specific language")
    group.add_argument("--update", action="store_true", help="Regenerate existing fixture tokens")
    group.add_argument("--list", action="store_true", help="List available languages and samples")

    args = parser.parse_args()

    if args.all:
        generate_all()
    elif args.language:
        generate_language(args.language)
    elif args.update:
        update_existing()
    elif args.list:
        list_available()


if __name__ == "__main__":
    main()

