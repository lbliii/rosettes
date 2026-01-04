# RFC: Fixture Expansion for Untested Languages

| Field | Value |
|-------|-------|
| **Status** | Draft |
| **Created** | 2026-01-04 |
| **Updated** | 2026-01-04 |
| **Author** | Bengal Team |
| **Scope** | Quality Assurance |
| **Goal** | Expand golden test fixtures from 16 to 55 languages |
| **Depends On** | rfc-test-hardening (Implemented) |

## Summary

Add golden test fixtures for the 39 languages currently lacking dedicated test coverage. Property-based tests (from rfc-test-hardening) verify *invariants*; fixtures verify *correctness* of token classification. This RFC expands coverage from 16 languages (29%) to all 55 languages (100%).

## Current State

### Fixture Coverage

**55 languages** in rosettes, but only **16 have fixtures** (29%):

| Coverage Level | Languages | Count | Fixture Files |
|----------------|-----------|-------|---------------|
| **Comprehensive** (6+ fixtures) | python, rust, javascript, kida | 4 | 25 fixtures |
| **Basic** (1 fixture) | bash, css, go, html, json, markdown, php, sql, toml, typescript, xml, yaml | 12 | 12 fixtures |
| **None** | 39 languages | 39 | 0 fixtures |

**Total**: 16 languages, 37 fixture files

### Languages Without Fixtures (39 total)

**Tier 1 (Critical)**: `java`, `cpp`, `c`, `ruby`, `swift`, `kotlin` (6)  
**Tier 2 (Popular)**: `dockerfile`, `graphql`, `hcl`, `scala`, `perl`, `lua` (6)  
**Tier 3 (Standard)**: `groovy`, `r`, `julia`, `elixir`, `haskell`, `nim`, `zig`, `v`, `dart`, `gleam` (10)  
**Tier 4 (Minimal)**: `ini`, `csv`, `diff`, `makefile`, `nginx`, `pkl`, `cue`, `protobuf`, `mojo`, `triton`, `stan`, `clojure`, `jinja`, `tree`, `powershell`, `plaintext`, `cuda` (17)

**Note**: `diff` is listed as missing but has a lexer; verify if fixture exists.

### Why Fixtures Matter

Property tests verify that lexers don't drop characters or crash. Fixtures verify that lexers **classify tokens correctly**:

```python
# Property test: ✅ passes for "<div>" tokenized as anything
assert "".join(t.value for t in tokens) == "<div>"

# Fixture test: ❌ fails if "<div>" is tokenized as ERROR instead of NAME_TAG
assert tokens[1].type == TokenType.NAME_TAG
```

## Design

### Tier-Based Approach

Prioritize by language popularity and complexity:

| Tier | Criteria | Languages | Fixtures Per Language |
|------|----------|-----------|----------------------|
| **1: Critical** | Top 10 usage, high complexity | java, cpp, c, ruby, swift, kotlin | 5-7 fixtures |
| **2: Popular** | Common in ecosystems | dockerfile, graphql, hcl, scala, perl, lua | 3-5 fixtures |
| **3: Standard** | Lower traffic, simpler grammars | groovy, r, julia, elixir, haskell, nim, zig, v, dart, gleam | 2-3 fixtures |
| **4: Minimal** | Config/data formats | ini, csv, diff, makefile, nginx, pkl, cue, protobuf, mojo, triton, stan, clojure, jinja, tree, powershell, plaintext | 1-2 fixtures |

### Fixture Categories

Each language should have fixtures covering (where applicable):

| Category | Purpose | Example Construct | Required For |
|----------|---------|-------------------|--------------|
| `basics` | Core language constructs | Variable declaration, function call | All languages |
| `keywords` | All keywords classified correctly | `if`, `class`, `return`, `async` | Languages with keywords |
| `strings` | String literal variants | Single, double, multiline, raw, interpolated | Languages with strings |
| `numbers` | Numeric literal variants | Int, float, hex, binary, scientific | Languages with numbers |
| `comments` | Comment styles | Single-line, multiline, doc comments | Languages with comments |
| `operators` | Operator classification | Arithmetic, comparison, logical | Languages with operators |
| `types` | Type annotations (if applicable) | Generics, union types | Typed languages |

**Language-Specific Categories** (add as needed):
- Java: `generics`, `annotations`, `lambdas`
- C/C++: `preprocessor`, `pointers`, `templates`
- Ruby: `blocks`, `symbols`, `regex`, `heredoc`
- Swift: `optionals`, `closures`, `propertyWrappers`
- Kotlin: `nullSafety`, `coroutines`, `extensions`, `sealed`
- Scala: `patternMatching`, `implicits`, `forComprehension`
- Perl: `regex`, `references`
- Lua: `metatables`, `coroutines`

### Fixture Format

Matches existing convention:

```
tests/fixtures/
├── java/
│   ├── basics.java
│   ├── basics.tokens.json
│   ├── keywords.java
│   ├── keywords.tokens.json
│   ├── strings.java
│   ├── strings.tokens.json
│   ├── generics.java
│   └── generics.tokens.json
```

**Token JSON format**:
```json
[
  {"type": "KEYWORD", "value": "public", "line": 1, "column": 1},
  {"type": "WHITESPACE", "value": " ", "line": 1, "column": 7},
  {"type": "KEYWORD", "value": "class", "line": 1, "column": 8}
]
```

**Token Type Standards**: All token types must use `TokenType` enum values (see `rosettes._types.TokenType`). Common types:
- Keywords: `KEYWORD`, `KEYWORD_CONSTANT`, `KEYWORD_DECLARATION`, `KEYWORD_TYPE`
- Names: `NAME`, `NAME_FUNCTION`, `NAME_CLASS`, `NAME_VARIABLE`, `NAME_BUILTIN`
- Strings: `STRING`, `STRING_SINGLE`, `STRING_DOUBLE`, `STRING_INTERPOL`
- Numbers: `NUMBER_INTEGER`, `NUMBER_FLOAT`, `NUMBER_HEX`, `NUMBER_BIN`
- Comments: `COMMENT`, `COMMENT_SINGLE`, `COMMENT_MULTILINE`
- Operators: `OPERATOR`, `OPERATOR_WORD`
- Punctuation: `PUNCTUATION`
- Special: `WHITESPACE`, `ERROR`, `TEXT`

**Note**: Token type names in JSON use the enum name (e.g., `"KEYWORD"`), not the CSS class value.

## Implementation Order

**Critical**: Complete Phase 0 (prerequisites) before creating fixtures manually.

**Recommended approach**:
1. **Phase 0**: Update `generate_fixtures.py` with all language samples
2. **Phase 1-4**: Generate fixtures using script, then manually refine/expand as needed
3. **Phase 5**: Create unified test infrastructure
4. **Phase 6**: Add CI validation

**Alternative approach** (if script update is delayed):
- Create fixtures manually following examples in each phase
- Update script later for regeneration capability

## Implementation

### Phase 0: Prerequisites (2 hours) ⚠️ **MUST COMPLETE FIRST**

**Goal**: Enable automated fixture generation for all languages.

**Tasks**:
1. Update `scripts/generate_fixtures.py`:
   - Add `LANGUAGE_SAMPLES` entries for all 39 missing languages
   - Add extension mappings in `EXTENSIONS` dict
   - Use code examples from Phase 1-4 sections below
2. Verify script works:
   ```bash
   uv run python scripts/generate_fixtures.py --language java
   ```
3. Test regeneration:
   ```bash
   uv run python scripts/generate_fixtures.py --update
   ```

**Deliverable**: `generate_fixtures.py` supports all 55 languages.

### Phase 1: Tier 1 Languages (4 hours)

#### 1.1 Java

```java
// tests/fixtures/java/basics.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// tests/fixtures/java/generics.java
public class Box<T extends Comparable<T>> {
    private T value;
    
    public <U> void process(List<? super U> items) {
        // Generic method
    }
}

// tests/fixtures/java/keywords.java
abstract class Example implements Runnable {
    private final int count;
    protected volatile boolean running;
    
    synchronized void process() throws Exception {
        if (running) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } finally {
                running = false;
            }
        }
    }
}

// tests/fixtures/java/annotations.java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    
    @Column(nullable = false)
    private String name;
}

// tests/fixtures/java/lambdas.java
List<String> filtered = items.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

#### 1.2 C/C++

```c
// tests/fixtures/c/basics.c
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, World!\n");
    return 0;
}

// tests/fixtures/c/preprocessor.c
#ifndef HEADER_H
#define HEADER_H

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define VERSION 1

#ifdef DEBUG
    #define LOG(msg) printf("%s\n", msg)
#else
    #define LOG(msg)
#endif

#pragma once

#endif

// tests/fixtures/c/pointers.c
void process(int *ptr, int **pptr, void (*callback)(int)) {
    int arr[10];
    int *p = &arr[0];
    *ptr = **pptr;
    callback(*p);
}

// tests/fixtures/cpp/classes.cpp
template<typename T>
class Container {
public:
    explicit Container(T value) : value_(std::move(value)) {}
    
    T& get() noexcept { return value_; }
    const T& get() const noexcept { return value_; }
    
private:
    T value_;
};

// tests/fixtures/cpp/modern.cpp
auto process(std::vector<int>&& items) -> std::optional<int> {
    if (auto it = std::ranges::find(items, 42); it != items.end()) {
        return *it;
    }
    return std::nullopt;
}

constexpr auto lambda = [](auto x) constexpr { return x * 2; };
```

#### 1.3 Ruby

```ruby
# tests/fixtures/ruby/basics.rb
class User
  attr_accessor :name, :email
  
  def initialize(name, email)
    @name = name
    @email = email
  end
  
  def greet
    puts "Hello, #{@name}!"
  end
end

# tests/fixtures/ruby/blocks.rb
items.each do |item|
  puts item
end

items.map { |x| x * 2 }

File.open("file.txt") do |f|
  f.each_line { |line| process(line) }
end

# tests/fixtures/ruby/symbols.rb
options = {
  name: "test",
  :legacy => "value",
  enabled: true
}

def method(arg, *args, **kwargs, &block)
  yield if block_given?
end

# tests/fixtures/ruby/regex.rb
pattern = /\A[a-z]+\z/i
text =~ /hello/
text.match?(/world/)
gsub(/old/, "new")

# tests/fixtures/ruby/heredoc.rb
sql = <<~SQL
  SELECT *
  FROM users
  WHERE active = true
SQL

html = <<-HTML
  <div>Content</div>
HTML
```

#### 1.4 Swift

```swift
// tests/fixtures/swift/basics.swift
import Foundation

struct User: Codable {
    let id: Int
    var name: String
    var email: String?
}

class UserService {
    func fetchUser(id: Int) async throws -> User {
        let url = URL(string: "https://api.example.com/users/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(User.self, from: data)
    }
}

// tests/fixtures/swift/optionals.swift
var name: String? = nil
let unwrapped = name ?? "default"
if let n = name {
    print(n)
}
guard let n = name else { return }

// tests/fixtures/swift/closures.swift
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let sorted = numbers.sorted { $0 > $1 }

func process(completion: @escaping (Result<Int, Error>) -> Void) {
    DispatchQueue.main.async {
        completion(.success(42))
    }
}

// tests/fixtures/swift/generics.swift
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

protocol Container {
    associatedtype Item
    var count: Int { get }
    mutating func append(_ item: Item)
}

// tests/fixtures/swift/propertyWrappers.swift
@propertyWrapper
struct Clamped<Value: Comparable> {
    var value: Value
    let range: ClosedRange<Value>
    
    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
}
```

#### 1.5 Kotlin

```kotlin
// tests/fixtures/kotlin/basics.kt
data class User(
    val id: Int,
    val name: String,
    val email: String?
)

fun main() {
    val user = User(1, "Alice", "alice@example.com")
    println("Hello, ${user.name}!")
}

// tests/fixtures/kotlin/nullSafety.kt
val name: String? = null
val length = name?.length ?: 0
val forced = name!!.length

name?.let { n ->
    println(n.uppercase())
}

// tests/fixtures/kotlin/coroutines.kt
suspend fun fetchData(): Result<String> = coroutineScope {
    val deferred = async {
        delay(100)
        "data"
    }
    Result.success(deferred.await())
}

fun main() = runBlocking {
    launch {
        fetchData().onSuccess { println(it) }
    }
}

// tests/fixtures/kotlin/extensions.kt
fun String.isPalindrome(): Boolean {
    return this == this.reversed()
}

val String.wordCount: Int
    get() = this.split("\\s+".toRegex()).size

// tests/fixtures/kotlin/sealed.kt
sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

fun <T> Result<T>.getOrNull(): T? = when (this) {
    is Result.Success -> value
    else -> null
}
```

### Phase 2: Tier 2 Languages (3 hours)

#### 2.1 Dockerfile

```dockerfile
# tests/fixtures/dockerfile/basics.dockerfile
FROM python:3.14-slim AS builder

ARG VERSION=1.0
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health

ENTRYPOINT ["python"]
CMD ["app.py"]

# tests/fixtures/dockerfile/multistage.dockerfile
FROM node:20 AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend /app/dist /usr/share/nginx/html
```

#### 2.2 GraphQL

```graphql
# tests/fixtures/graphql/schema.graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User
  deleteUser(id: ID!): Boolean!
}

type User implements Node {
  id: ID!
  name: String!
  email: String!
  posts(first: Int): [Post!]!
  createdAt: DateTime!
}

input CreateUserInput {
  name: String!
  email: String!
}

interface Node {
  id: ID!
}

union SearchResult = User | Post | Comment

enum Role {
  ADMIN
  USER
  GUEST
}

scalar DateTime

directive @auth(requires: Role = ADMIN) on FIELD_DEFINITION
```

#### 2.3 HCL (Terraform)

```hcl
# tests/fixtures/hcl/basics.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region"
}

resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  tags = {
    Name        = "web-${count.index}"
    Environment = var.environment
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }
}

output "instance_ids" {
  value       = aws_instance.web[*].id
  description = "IDs of created instances"
}

locals {
  common_tags = {
    Project = "example"
    Owner   = "team"
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

#### 2.4 Scala

```scala
// tests/fixtures/scala/basics.scala
package com.example

import scala.concurrent.{Future, ExecutionContext}
import scala.util.{Try, Success, Failure}

case class User(id: Long, name: String, email: Option[String])

object UserService {
  def findById(id: Long)(implicit ec: ExecutionContext): Future[Option[User]] = Future {
    Some(User(id, "Alice", Some("alice@example.com")))
  }
}

// tests/fixtures/scala/patternMatching.scala
def process(value: Any): String = value match {
  case i: Int if i > 0 => s"Positive: $i"
  case s: String => s.toUpperCase
  case Some(x) => s"Got: $x"
  case None => "Nothing"
  case (a, b) => s"Tuple: $a, $b"
  case head :: tail => s"List head: $head"
  case _ => "Unknown"
}

// tests/fixtures/scala/implicits.scala
implicit class RichString(s: String) {
  def isPalindrome: Boolean = s == s.reverse
}

implicit val defaultTimeout: Duration = 5.seconds

def fetch(url: String)(implicit timeout: Duration): String = ???

// tests/fixtures/scala/forComprehension.scala
for {
  user <- findUser(id)
  profile <- fetchProfile(user.id)
  preferences <- loadPreferences(user.id)
} yield UserDetails(user, profile, preferences)
```

#### 2.5 Perl

```perl
# tests/fixtures/perl/basics.pl
#!/usr/bin/env perl
use strict;
use warnings;
use feature 'say';

my $name = "World";
say "Hello, $name!";

my @items = (1, 2, 3, 4, 5);
my %hash = (key => 'value', foo => 'bar');

sub greet {
    my ($name, $greeting) = @_;
    $greeting //= "Hello";
    return "$greeting, $name!";
}

# tests/fixtures/perl/regex.pl
if ($text =~ /pattern/) {
    print "Match!\n";
}

$text =~ s/old/new/g;
$text =~ tr/a-z/A-Z/;

my @matches = $text =~ /(\w+)/g;

# tests/fixtures/perl/references.pl
my $scalar_ref = \$scalar;
my $array_ref = \@array;
my $hash_ref = \%hash;
my $code_ref = \&subroutine;

my $anon_array = [1, 2, 3];
my $anon_hash = {key => 'value'};
my $anon_sub = sub { return $_[0] * 2 };

print $$scalar_ref;
print $array_ref->[0];
print $hash_ref->{key};
$code_ref->();
```

#### 2.6 Lua

```lua
-- tests/fixtures/lua/basics.lua
local function greet(name)
    name = name or "World"
    print("Hello, " .. name .. "!")
end

local items = {1, 2, 3, 4, 5}
local config = {
    host = "localhost",
    port = 8080,
    enabled = true
}

for i, v in ipairs(items) do
    print(i, v)
end

for k, v in pairs(config) do
    print(k .. " = " .. tostring(v))
end

-- tests/fixtures/lua/metatables.lua
local Vector = {}
Vector.__index = Vector

function Vector.new(x, y)
    return setmetatable({x = x, y = y}, Vector)
end

function Vector:length()
    return math.sqrt(self.x^2 + self.y^2)
end

function Vector.__add(a, b)
    return Vector.new(a.x + b.x, a.y + b.y)
end

-- tests/fixtures/lua/coroutines.lua
local co = coroutine.create(function()
    for i = 1, 10 do
        coroutine.yield(i)
    end
end)

while coroutine.status(co) ~= "dead" do
    local ok, value = coroutine.resume(co)
    if ok then print(value) end
end
```

### Phase 3: Tier 3 Languages (2 hours)

Create 2-3 fixtures each for: `groovy`, `r`, `julia`, `elixir`, `haskell`, `nim`, `zig`, `v`, `dart`, `gleam`

Example for Elixir:

```elixir
# tests/fixtures/elixir/basics.ex
defmodule User do
  @moduledoc "User module"
  
  defstruct [:id, :name, :email]
  
  def new(name, email) do
    %__MODULE__{id: UUID.uuid4(), name: name, email: email}
  end
  
  def greet(%__MODULE__{name: name}) do
    "Hello, #{name}!"
  end
end

# tests/fixtures/elixir/patternMatching.ex
def process(value) do
  case value do
    {:ok, result} -> result
    {:error, reason} -> raise reason
    [head | _tail] -> head
    %{key: value} -> value
    _ -> nil
  end
end

def handle_message({:ping, sender}), do: send(sender, :pong)
def handle_message({:data, payload}), do: process(payload)
def handle_message(_), do: :ignore

# tests/fixtures/elixir/pipes.ex
result =
  data
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
  |> Enum.reduce(0, &+/2)
```

### Phase 4: Tier 4 Languages (1 hour)

Create 1-2 basic fixtures each for remaining languages:

```ini
; tests/fixtures/ini/basics.ini
[section]
key = value
number = 42
boolean = true

[database]
host = localhost
port = 5432
```

```csv
# tests/fixtures/csv/basics.csv
name,age,email
Alice,30,alice@example.com
Bob,25,bob@example.com
```

```diff
# tests/fixtures/diff/basics.diff
--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,4 @@
 unchanged
-removed line
+added line
+another added
 unchanged
```

### Phase 5: Test Infrastructure (1.5 hours)

#### 5.1 Test Infrastructure Strategy

**Decision**: Create unified `test_fixtures.py` that complements (does not replace) existing language-specific tests.

**Rationale**:
- Existing `test_*_sm.py` files provide detailed, language-specific test coverage
- Unified test provides discovery and regression testing across all fixtures
- Both patterns serve different purposes:
  - Language-specific: Deep testing of language constructs
  - Unified: Broad coverage verification and CI regression testing

**Integration**:
- Unified test uses `discover_fixtures()` to find all fixtures automatically
- Language-specific tests continue using `load_fixture()` helper from `conftest.py`
- Both test patterns can coexist and complement each other

#### 5.2 Parameterized fixture tests

```python
# tests/lexers/test_fixtures.py
"""Unified test runner for all lexer fixtures.

This test file discovers and validates all fixtures across all languages.
Complements language-specific tests in test_*_sm.py files.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rosettes import get_lexer

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def discover_fixtures():
    """Discover all fixture pairs (source + tokens).
    
    Returns:
        List of tuples: (language, fixture_name, source_file, tokens_file)
    """
    fixtures = []
    if not FIXTURES_DIR.exists():
        return fixtures
    
    for lang_dir in sorted(FIXTURES_DIR.iterdir()):
        if not lang_dir.is_dir():
            continue
        language = lang_dir.name
        
        for tokens_file in sorted(lang_dir.glob("*.tokens.json")):
            name = tokens_file.stem.replace(".tokens", "")
            
            # Find corresponding source file (try common extensions)
            source_file = None
            for ext in [".py", ".js", ".ts", ".rs", ".go", ".java", ".kt", ".swift", 
                       ".rb", ".pl", ".lua", ".scala", ".ex", ".hs", ".nim", ".zig",
                       ".v", ".dart", ".gleam", ".yaml", ".json", ".php", ".sh", 
                       ".sql", ".toml", ".xml", ".html", ".css", ".md", ".kida",
                       ".c", ".cpp", ".h", ".hpp", ".dockerfile", ".graphql", ".tf",
                       ".ini", ".csv", ".diff", ".makefile", ".nginx", ".proto",
                       ".mojo", ".triton", ".cu", ".stan", ".pkl", ".cue", ".clj",
                       ".jinja", ".tree", ".ps1", ".txt"]:
                candidate = lang_dir / f"{name}{ext}"
                if candidate.exists():
                    source_file = candidate
                    break
            
            if source_file:
                fixtures.append((language, name, source_file, tokens_file))
    
    return fixtures


FIXTURES = discover_fixtures()


@pytest.mark.parametrize("language,name,source_file,tokens_file", FIXTURES)
def test_fixture_token_types(language, name, source_file, tokens_file):
    """Verify token types match expected fixture."""
    lexer = get_lexer(language)
    source = source_file.read_text(encoding="utf-8")
    
    try:
        expected_json = tokens_file.read_text(encoding="utf-8")
        expected = json.loads(expected_json)
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON in {tokens_file}: {e}")
    
    actual = list(lexer.tokenize(source))
    
    # First verify count matches
    assert len(actual) == len(expected), (
        f"Token count mismatch for {language}/{name}: "
        f"got {len(actual)}, expected {len(expected)}\n"
        f"Source: {source_file}\n"
        f"Tokens: {tokens_file}"
    )
    
    # Then verify each token
    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act.type.name == exp["type"], (
            f"Token {i} type mismatch in {language}/{name}: "
            f"got {act.type.name}, expected {exp['type']} "
            f"for value {act.value!r} at line {act.line}, column {act.column}"
        )
        assert act.value == exp["value"], (
            f"Token {i} value mismatch in {language}/{name}: "
            f"got {act.value!r}, expected {exp['value']!r} "
            f"at line {act.line}, column {act.column}"
        )
        # Optionally verify line/column if present in expected
        if "line" in exp:
            assert act.line == exp["line"], (
                f"Token {i} line mismatch in {language}/{name}: "
                f"got {act.line}, expected {exp['line']}"
            )
        if "column" in exp:
            assert act.column == exp["column"], (
                f"Token {i} column mismatch in {language}/{name}: "
                f"got {act.column}, expected {exp['column']}"
            )


@pytest.mark.parametrize("language,name,source_file,tokens_file", FIXTURES)
def test_fixture_reconstructs(language, name, source_file, tokens_file):
    """Verify tokenization reconstructs original source (invariant check)."""
    lexer = get_lexer(language)
    source = source_file.read_text(encoding="utf-8")
    
    tokens = list(lexer.tokenize(source))
    reconstructed = "".join(t.value for t in tokens)
    
    assert reconstructed == source, (
        f"Reconstruction failed for {language}/{name}: "
        f"source length {len(source)}, reconstructed length {len(reconstructed)}"
    )
```

#### 5.3 Fixture generation script update

**Priority**: Update `scripts/generate_fixtures.py` **before** creating fixtures to enable automated generation.

**Required Updates**:
1. Add `LANGUAGE_SAMPLES` entries for all 39 missing languages
2. Add extension mappings for all languages
3. Ensure samples cover language-specific constructs (see Phase examples)

**Example Structure**:
```python
# scripts/generate_fixtures.py additions

LANGUAGE_SAMPLES.update({
    "java": {
        "basics": '''public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
        "generics": '''public class Box<T extends Comparable<T>> {
    private T value;
    public <U> void process(List<? super U> items) {}
}''',
        "keywords": '''abstract class Example implements Runnable {
    private final int count;
    protected volatile boolean running;
    synchronized void process() throws Exception {
        if (running) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } finally {
                running = false;
            }
        }
    }
}''',
        "annotations": '''@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    @Column(nullable = false)
    private String name;
}''',
        "lambdas": '''List<String> filtered = items.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());''',
    },
    # ... continue for all 39 languages
})

EXTENSIONS.update({
    "java": ".java",
    "cpp": ".cpp",
    "c": ".c",
    "ruby": ".rb",
    "swift": ".swift",
    "kotlin": ".kt",
    # ... etc for all languages
})
```

**Usage**:
```bash
# Generate all fixtures
uv run python scripts/generate_fixtures.py --all

# Generate for specific language
uv run python scripts/generate_fixtures.py --language java

# Regenerate tokens for existing source files (after lexer changes)
uv run python scripts/generate_fixtures.py --update
```

### Phase 6: CI Updates (30 min)

Add comprehensive fixture validation to CI:

```yaml
# .github/workflows/test.yml
jobs:
  test:
    steps:
      - name: Verify fixture coverage
        run: |
          # Count languages with fixtures
          LANG_COUNT=$(find tests/fixtures -type d -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')
          FIXTURE_COUNT=$(find tests/fixtures -name "*.tokens.json" | wc -l | tr -d ' ')
          
          echo "Languages with fixtures: $LANG_COUNT/55"
          echo "Total fixture files: $FIXTURE_COUNT"
          
          # Verify tier coverage
          TIER1_LANGS="java cpp c ruby swift kotlin"
          TIER1_COUNT=0
          for lang in $TIER1_LANGS; do
            if [ -d "tests/fixtures/$lang" ]; then
              count=$(find "tests/fixtures/$lang" -name "*.tokens.json" | wc -l | tr -d ' ')
              if [ "$count" -ge 5 ]; then
                TIER1_COUNT=$((TIER1_COUNT + 1))
              fi
            fi
          done
          echo "Tier 1 coverage: $TIER1_COUNT/6 languages with 5+ fixtures"
          
          # Verify all languages have at least 1 fixture
          if [ "$LANG_COUNT" -lt 55 ]; then
            echo "::warning::Missing fixtures for $((55 - LANG_COUNT)) languages"
          fi
          
          # Verify JSON syntax
          echo "Validating JSON syntax..."
          for json_file in tests/fixtures/**/*.tokens.json; do
            python -m json.tool "$json_file" > /dev/null || {
              echo "::error::Invalid JSON: $json_file"
              exit 1
            }
          done
      
      - name: Run fixture tests
        run: uv run pytest tests/lexers/test_fixtures.py -v
      
      - name: Verify fixture completeness
        run: |
          # Check that every .tokens.json has a corresponding source file
          for tokens_file in tests/fixtures/**/*.tokens.json; do
            base="${tokens_file%.tokens.json}"
            found=false
            for ext in .py .js .ts .rs .go .java .kt .swift .rb .pl .lua .scala .ex .hs .nim .zig .v .dart .gleam .yaml .json .php .sh .sql .toml .xml .html .css .md .kida .c .cpp .h .hpp .dockerfile .graphql .tf .ini .csv .diff .makefile .nginx .proto .mojo .triton .cu .stan .pkl .cue .clj .jinja .tree .ps1 .txt; do
              if [ -f "${base}${ext}" ]; then
                found=true
                break
              fi
            done
            if [ "$found" = false ]; then
              echo "::warning::Missing source file for $tokens_file"
            fi
          done
```

## Success Criteria

| Criterion | Target | Current | Verification |
|-----------|--------|---------|--------------|
| **Languages with fixtures** | 55/55 (100%) | 16/55 (29%) | Count fixture directories |
| **Tier 1 coverage** | 5+ fixtures each | 0/6 | Verify per language |
| **Tier 2 coverage** | 3+ fixtures each | 0/6 | Verify per language |
| **Tier 3 coverage** | 2+ fixtures each | 0/10 | Verify per language |
| **Tier 4 coverage** | 1+ fixture each | 0/17 | Verify per language |
| **Fixture tests pass** | 100% | N/A | Run `pytest tests/lexers/test_fixtures.py` |
| **JSON syntax valid** | 100% | N/A | CI validation |
| **Source files exist** | 100% | N/A | CI validation |

## Timeline

| Phase | Duration | Deliverables | Notes |
|-------|----------|-------------|-------|
| 0: Prerequisites | 2 hours | Update `generate_fixtures.py` with all 39 language samples | **Must complete first** |
| 1: Tier 1 (Critical) | 4 hours | java, cpp, c, ruby, swift, kotlin fixtures (30-40 fixtures) | 5-7 fixtures per language |
| 2: Tier 2 (Popular) | 3 hours | dockerfile, graphql, hcl, scala, perl, lua fixtures (18-30 fixtures) | 3-5 fixtures per language |
| 3: Tier 3 (Standard) | 3 hours | 10 language fixtures (20-30 fixtures) | 2-3 fixtures per language |
| 4: Tier 4 (Minimal) | 2 hours | 17 language fixtures (17-34 fixtures) | 1-2 fixtures per language |
| 5: Test infrastructure | 1.5 hours | Unified test runner + integration | Complements existing tests |
| 6: CI updates | 30 min | Comprehensive fixture validation | JSON syntax, coverage checks |
| **Total** | ~16 hours | 39 new languages, 85-134 new fixtures | Includes prerequisite work |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fixture maintenance burden | Medium | JSON format enables automated regeneration via `generate_fixtures.py --update` |
| Token type disagreements | Medium | Document token type standards; use `TokenType` enum consistently; review process for edge cases |
| Lexer bugs exposed | Good | Fix bugs, add regression tests; fixtures serve as regression tests |
| Large PR size | Medium | Split by tier into separate PRs (Phase 1-4 can be separate PRs) |
| Missing language samples | High | **Prerequisite**: Update `generate_fixtures.py` before creating fixtures |
| Test infrastructure confusion | Low | Document that unified tests complement (not replace) language-specific tests |
| CI validation failures | Low | Comprehensive validation script catches issues early |
| Token type drift | Medium | Regular regeneration with `--update` flag; CI validates consistency |

## Decision Log

| Decision | Rationale |
|----------|-----------|
| **Tier-based prioritization** | Focus effort on highest-impact languages first (usage + complexity) |
| **JSON fixtures over inline** | Machine-readable, regeneratable, diffable; enables automated generation |
| **2-7 fixtures per language** | Balance coverage vs maintenance cost; tier-based minimums |
| **Unified + language-specific tests** | Unified tests for discovery/regression; language-specific for deep testing |
| **Token type standards** | Use `TokenType` enum consistently; document expected types per language |
| **Prerequisite: update generate_fixtures.py** | Enables automated fixture generation; reduces manual work |
| **Comprehensive CI validation** | Catches JSON syntax errors, missing files, coverage gaps early |

## Maintenance Strategy

### Regeneration Workflow

**When to regenerate fixtures**:
- After lexer changes that affect tokenization
- After fixing tokenization bugs
- When adding new language features to lexers
- Periodically to catch drift (quarterly review)

**How to regenerate**:
```bash
# Regenerate all existing fixtures
uv run python scripts/generate_fixtures.py --update

# Regenerate specific language
uv run python scripts/generate_fixtures.py --language java --update

# Verify changes
git diff tests/fixtures/
```

**Review process**:
1. Run regeneration
2. Review `git diff` for expected vs unexpected changes
3. Expected: Token type improvements, bug fixes
4. Unexpected: Token count changes, value changes (may indicate bugs)
5. Commit with descriptive message: `tests(fixtures): regenerate tokens after [change]`

### Handling Breaking Changes

**Scenario**: Lexer change causes tokenization differences

**Process**:
1. **Intentional changes**: Update fixtures, document rationale in commit
2. **Bug fixes**: Update fixtures, add regression test if needed
3. **Unintended changes**: Investigate lexer change, revert if needed, or update fixtures if change is correct

**Example commit message**:
```
tests(fixtures): update java generics tokens after lexer improvement

Lexer now correctly tokenizes generic type bounds as KEYWORD_TYPE.
Updated fixtures to reflect correct tokenization.
```

### Fixture Quality Guidelines

**Good fixtures**:
- ✅ Cover language-specific constructs (generics, lambdas, pattern matching)
- ✅ Include edge cases (empty strings, nested structures, special characters)
- ✅ Use realistic code examples (not contrived)
- ✅ Verify token types match language semantics
- ✅ Include comments explaining non-obvious constructs

**Bad fixtures**:
- ❌ Only trivial examples (single keywords, no context)
- ❌ Missing language-specific features (e.g., Java without generics)
- ❌ Overly complex examples (hard to verify correctness)
- ❌ Duplicate coverage (multiple fixtures testing same construct)

**Minimum coverage per tier**:
- **Tier 1**: 5+ fixtures covering basics, keywords, strings, numbers, language-specific features
- **Tier 2**: 3+ fixtures covering basics, keywords, and 1-2 language-specific features
- **Tier 3**: 2+ fixtures covering basics and 1 language-specific feature
- **Tier 4**: 1+ fixture covering basic syntax

### Versioning Strategy

**Current approach**: Fixtures are versioned with code (no separate versioning)

**Rationale**:
- Fixtures are tightly coupled to lexer implementation
- Git history provides version tracking
- Regeneration keeps fixtures in sync with lexers

**Future consideration**: If lexer API changes significantly, consider fixture versioning scheme.

## References

- Existing fixtures: `tests/fixtures/` (16 languages, 37 fixtures)
- Property tests: `tests/properties/test_lexer_invariants.py`
- Fixture generation: `scripts/generate_fixtures.py`
- Token types: `rosettes._types.TokenType`
- Test infrastructure: `tests/lexers/conftest.py` (load_fixture helper)
- Language-specific tests: `tests/lexers/test_*_sm.py`
- Related RFC: `plan/rfc-test-hardening.md` (Implemented)

