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
    # Tier 1: Critical languages
    "java": {
        "basics": '''public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
        "generics": '''public class Box<T extends Comparable<T>> {
    private T value;
    
    public <U> void process(List<? super U> items) {
        // Generic method
    }
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
    "cpp": {
        "classes": '''template<typename T>
class Container {
public:
    explicit Container(T value) : value_(std::move(value)) {}
    
    T& get() noexcept { return value_; }
    const T& get() const noexcept { return value_; }
    
private:
    T value_;
};''',
        "modern": '''auto process(std::vector<int>&& items) -> std::optional<int> {
    if (auto it = std::ranges::find(items, 42); it != items.end()) {
        return *it;
    }
    return std::nullopt;
}

constexpr auto lambda = [](auto x) constexpr { return x * 2; };''',
    },
    "c": {
        "basics": '''#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, World!\\n");
    return 0;
}''',
        "preprocessor": '''#ifndef HEADER_H
#define HEADER_H

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define VERSION 1

#ifdef DEBUG
    #define LOG(msg) printf("%s\\n", msg)
#else
    #define LOG(msg)
#endif

#pragma once

#endif''',
        "pointers": '''void process(int *ptr, int **pptr, void (*callback)(int)) {
    int arr[10];
    int *p = &arr[0];
    *ptr = **pptr;
    callback(*p);
}''',
    },
    "ruby": {
        "basics": '''class User
  attr_accessor :name, :email
  
  def initialize(name, email)
    @name = name
    @email = email
  end
  
  def greet
    puts "Hello, #{@name}!"
  end
end''',
        "blocks": '''items.each do |item|
  puts item
end

items.map { |x| x * 2 }

File.open("file.txt") do |f|
  f.each_line { |line| process(line) }
end''',
        "symbols": '''options = {
  name: "test",
  :legacy => "value",
  enabled: true
}

def method(arg, *args, **kwargs, &block)
  yield if block_given?
end''',
        "regex": '''pattern = /\\A[a-z]+\\z/i
text =~ /hello/
text.match?(/world/)
gsub(/old/, "new")''',
        "heredoc": '''sql = <<~SQL
  SELECT *
  FROM users
  WHERE active = true
SQL

html = <<-HTML
  <div>Content</div>
HTML''',
    },
    "swift": {
        "basics": '''import Foundation

struct User: Codable {
    let id: Int
    var name: String
    var email: String?
}

class UserService {
    func fetchUser(id: Int) async throws -> User {
        let url = URL(string: "https://api.example.com/users/\\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(User.self, from: data)
    }
}''',
        "optionals": '''var name: String? = nil
let unwrapped = name ?? "default"
if let n = name {
    print(n)
}
guard let n = name else { return }''',
        "closures": '''let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let sorted = numbers.sorted { $0 > $1 }

func process(completion: @escaping (Result<Int, Error>) -> Void) {
    DispatchQueue.main.async {
        completion(.success(42))
    }
}''',
        "generics": '''func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

protocol Container {
    associatedtype Item
    var count: Int { get }
    mutating func append(_ item: Item)
}''',
        "propertyWrappers": '''@propertyWrapper
struct Clamped<Value: Comparable> {
    var value: Value
    let range: ClosedRange<Value>
    
    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
}''',
    },
    "kotlin": {
        "basics": '''data class User(
    val id: Int,
    val name: String,
    val email: String?
)

fun main() {
    val user = User(1, "Alice", "alice@example.com")
    println("Hello, ${user.name}!")
}''',
        "nullSafety": '''val name: String? = null
val length = name?.length ?: 0
val forced = name!!.length

name?.let { n ->
    println(n.uppercase())
}''',
        "coroutines": '''suspend fun fetchData(): Result<String> = coroutineScope {
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
}''',
        "extensions": '''fun String.isPalindrome(): Boolean {
    return this == this.reversed()
}

val String.wordCount: Int
    get() = this.split("\\\\s+".toRegex()).size''',
        "sealed": '''sealed class Result<out T> {
    data class Success<T>(val value: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

fun <T> Result<T>.getOrNull(): T? = when (this) {
    is Result.Success -> value
    else -> null
}''',
    },
    # Tier 2: Popular languages
    "dockerfile": {
        "basics": '''FROM python:3.14-slim AS builder

ARG VERSION=1.0
ENV APP_HOME=/app \\
    PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health

ENTRYPOINT ["python"]
CMD ["app.py"]''',
        "multistage": '''FROM node:20 AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=frontend /app/dist /usr/share/nginx/html''',
    },
    "graphql": {
        "schema": '''type Query {
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

directive @auth(requires: Role = ADMIN) on FIELD_DEFINITION''',
    },
    "hcl": {
        "basics": '''terraform {
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
}''',
    },
    "scala": {
        "basics": '''package com.example

import scala.concurrent.{Future, ExecutionContext}
import scala.util.{Try, Success, Failure}

case class User(id: Long, name: String, email: Option[String])

object UserService {
  def findById(id: Long)(implicit ec: ExecutionContext): Future[Option[User]] = Future {
    Some(User(id, "Alice", Some("alice@example.com")))
  }
}''',
        "patternMatching": '''def process(value: Any): String = value match {
  case i: Int if i > 0 => s"Positive: $i"
  case s: String => s.toUpperCase
  case Some(x) => s"Got: $x"
  case None => "Nothing"
  case (a, b) => s"Tuple: $a, $b"
  case head :: tail => s"List head: $head"
  case _ => "Unknown"
}''',
        "implicits": '''implicit class RichString(s: String) {
  def isPalindrome: Boolean = s == s.reverse
}

implicit val defaultTimeout: Duration = 5.seconds

def fetch(url: String)(implicit timeout: Duration): String = ???''',
        "forComprehension": '''for {
  user <- findUser(id)
  profile <- fetchProfile(user.id)
  preferences <- loadPreferences(user.id)
} yield UserDetails(user, profile, preferences)''',
    },
    "perl": {
        "basics": '''#!/usr/bin/env perl
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
}''',
        "regex": '''if ($text =~ /pattern/) {
    print "Match!\\n";
}

$text =~ s/old/new/g;
$text =~ tr/a-z/A-Z/;

my @matches = $text =~ /(\\w+)/g;''',
        "references": '''my $scalar_ref = \\$scalar;
my $array_ref = \\@array;
my $hash_ref = \\%hash;
my $code_ref = \\&subroutine;

my $anon_array = [1, 2, 3];
my $anon_hash = {key => 'value'};
my $anon_sub = sub { return $_[0] * 2 };

print $$scalar_ref;
print $array_ref->[0];
print $hash_ref->{key};
$code_ref->();''',
    },
    "lua": {
        "basics": '''local function greet(name)
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
end''',
        "metatables": '''local Vector = {}
Vector.__index = Vector

function Vector.new(x, y)
    return setmetatable({x = x, y = y}, Vector)
end

function Vector:length()
    return math.sqrt(self.x^2 + self.y^2)
end

function Vector.__add(a, b)
    return Vector.new(a.x + b.x, a.y + b.y)
end''',
        "coroutines": '''local co = coroutine.create(function()
    for i = 1, 10 do
        coroutine.yield(i)
    end
end)

while coroutine.status(co) ~= "dead" do
    local ok, value = coroutine.resume(co)
    if ok then print(value) end
end''',
    },
    # Tier 3: Standard languages
    "groovy": {
        "basics": '''class User {
    String name
    String email
    
    User(String name, String email) {
        this.name = name
        this.email = email
    }
    
    String greet() {
        "Hello, ${name}!"
    }
}

def user = new User("Alice", "alice@example.com")
println user.greet()''',
        "closures": '''def numbers = [1, 2, 3, 4, 5]
def doubled = numbers.collect { it * 2 }
def filtered = numbers.findAll { it > 2 }

numbers.each { n ->
    println n
}''',
    },
    "r": {
        "basics": '''# Variables and assignment
x <- 42
y <- 3.14
name <- "Alice"

# Functions
greet <- function(name) {
    paste("Hello,", name, "!")
}

result <- greet(name)

# Vectors
numbers <- c(1, 2, 3, 4, 5)
doubled <- numbers * 2

# Data frames
df <- data.frame(
    name = c("Alice", "Bob"),
    age = c(30, 25)
)''',
        "statistics": '''# Statistical operations
mean_value <- mean(numbers)
sd_value <- sd(numbers)

# Linear model
model <- lm(y ~ x, data = df)
summary(model)''',
    },
    "julia": {
        "basics": '''struct User
    id::Int
    name::String
    email::Union{String, Nothing}
end

function greet(user::User)
    println("Hello, $(user.name)!")
end

user = User(1, "Alice", "alice@example.com")
greet(user)''',
        "multipleDispatch": '''abstract type Shape end

struct Circle <: Shape
    radius::Float64
end

struct Rectangle <: Shape
    width::Float64
    height::Float64
end

area(s::Circle) = π * s.radius^2
area(s::Rectangle) = s.width * s.height''',
    },
    "elixir": {
        "basics": '''defmodule User do
  @moduledoc "User module"
  
  defstruct [:id, :name, :email]
  
  def new(name, email) do
    %__MODULE__{id: UUID.uuid4(), name: name, email: email}
  end
  
  def greet(%__MODULE__{name: name}) do
    "Hello, #{name}!"
  end
end''',
        "patternMatching": '''def process(value) do
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
def handle_message(_), do: :ignore''',
        "pipes": '''result =
  data
  |> Enum.filter(&(&1 > 0))
  |> Enum.map(&(&1 * 2))
  |> Enum.reduce(0, &+/2)''',
    },
    "haskell": {
        "basics": '''data User = User
    { userId :: Int
    , userName :: String
    , userEmail :: Maybe String
    }

greet :: User -> String
greet user = "Hello, " ++ userName user ++ "!"

main :: IO ()
main = do
    let user = User 1 "Alice" (Just "alice@example.com")
    putStrLn $ greet user''',
        "typeclasses": '''class Show a where
    show :: a -> String

instance Show User where
    show (User id name email) = name

instance Functor Maybe where
    fmap f Nothing = Nothing
    fmap f (Just x) = Just (f x)''',
    },
    "nim": {
        "basics": '''type
  User = object
    id: int
    name: string
    email: Option[string]

proc greet(user: User): string =
  "Hello, " & user.name & "!"

let user = User(id: 1, name: "Alice", email: some("alice@example.com"))
echo greet(user)''',
        "generics": '''proc swap[T](a, b: var T) =
  let temp = a
  a = b
  b = temp

type
  Container[T] = object
    value: T''',
    },
    "zig": {
        "basics": '''const std = @import("std");

const User = struct {
    id: u32,
    name: []const u8,
    email: ?[]const u8,
};

pub fn main() !void {
    const user = User{
        .id = 1,
        .name = "Alice",
        .email = "alice@example.com",
    };
    std.debug.print("Hello, {s}!\\n", .{user.name});
}''',
        "comptime": '''fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

const result = max(u32, 10, 20);''',
    },
    "v": {
        "basics": '''struct User {
    id int
    name string
    email ?string
}

fn greet(user User) string {
    return "Hello, ${user.name}!"
}

fn main() {
    user := User{
        id: 1
        name: "Alice"
        email: "alice@example.com"
    }
    println(greet(user))
}''',
        "interfaces": '''interface Drawable {
    draw()
}

struct Circle {
    radius f64
}

fn (c Circle) draw() {
    println("Drawing circle")
}''',
    },
    "dart": {
        "basics": '''class User {
  final int id;
  final String name;
  final String? email;
  
  User(this.id, this.name, this.email);
  
  String greet() {
    return "Hello, $name!";
  }
}

void main() {
  final user = User(1, "Alice", "alice@example.com");
  print(user.greet());
}''',
        "async": '''Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 1));
  return "data";
}

void main() async {
  final data = await fetchData();
  print(data);
}''',
    },
    "gleam": {
        "basics": '''import gleam/io

pub type User {
  User(id: Int, name: String, email: Option(String))
}

pub fn greet(user: User) {
  case user {
    User(_, name, _) -> "Hello, " <> name <> "!"
  }
}

pub fn main() {
  let user = User(1, "Alice", Some("alice@example.com"))
  io.println(greet(user))
}''',
        "patternMatching": '''pub fn process(value: Result(String, String)) {
  case value {
    Ok(result) -> result
    Error(reason) -> "Error: " <> reason
  }
}''',
    },
    # Tier 4: Minimal languages
    "ini": {
        "basics": '''; Configuration file
[section]
key = value
number = 42
boolean = true

[database]
host = localhost
port = 5432''',
    },
    "csv": {
        "basics": '''name,age,email
Alice,30,alice@example.com
Bob,25,bob@example.com''',
    },
    "diff": {
        "basics": '''--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,4 @@
 unchanged
-removed line
+added line
+another added
 unchanged''',
    },
    "makefile": {
        "basics": '''CC = gcc
CFLAGS = -Wall -g

all: program

program: main.o utils.o
\t$(CC) $(CFLAGS) -o program main.o utils.o

main.o: main.c
\t$(CC) $(CFLAGS) -c main.c

clean:
\trm -f *.o program

.PHONY: all clean''',
    },
    "nginx": {
        "basics": '''server {
    listen 80;
    server_name example.com;
    
    location / {
        root /var/www/html;
        index index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8080;
    }
}''',
    },
    "pkl": {
        "basics": '''amends "package://pkl-lang/pkl-python@1.0.0"

name = "my-app"
version = "1.0.0"

dependencies {
    ["requests"] = "2.28.0"
}

server {
    host = "localhost"
    port = 8080
}''',
    },
    "cue": {
        "basics": '''package example

#User: {
    id: int
    name: string
    email?: string
}

user: #User & {
    id: 1
    name: "Alice"
}''',
    },
    "protobuf": {
        "basics": '''syntax = "proto3";

package example;

message User {
    int32 id = 1;
    string name = 2;
    string email = 3;
}

service UserService {
    rpc GetUser(UserRequest) returns (User);
}''',
    },
    "mojo": {
        "basics": '''struct User:
    var id: Int
    var name: String
    var email: String
    
    fn __init__(inout self, id: Int, name: String, email: String):
        self.id = id
        self.name = name
        self.email = email

fn main():
    let user = User(1, "Alice", "alice@example.com")
    print("Hello,", user.name)''',
    },
    "triton": {
        "basics": '''import triton

@triton.jit
def add_kernel(x_ptr, y_ptr, output_ptr, n_elements, BLOCK_SIZE: "constexpr"):
    pid = triton.program_id(0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + triton.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = triton.load(x_ptr + offsets, mask=mask)
    y = triton.load(y_ptr + offsets, mask=mask)
    output = x + y
    triton.store(output_ptr + offsets, output, mask=mask)''',
    },
    "stan": {
        "basics": '''data {
    int<lower=0> N;
    vector[N] x;
    vector[N] y;
}

parameters {
    real alpha;
    real beta;
    real<lower=0> sigma;
}

model {
    alpha ~ normal(0, 1);
    beta ~ normal(0, 1);
    sigma ~ exponential(1);
    y ~ normal(alpha + beta * x, sigma);
}''',
    },
    "clojure": {
        "basics": '''(ns example.user
  (:require [clojure.string :as str]))

(defrecord User [id name email])

(defn greet [user]
  (str "Hello, " (:name user) "!"))

(def user (->User 1 "Alice" "alice@example.com"))
(println (greet user))''',
        "macros": '''(defmacro when [test & body]
  `(if ~test (do ~@body)))

(when true
  (println "It's true!"))''',
    },
    "jinja": {
        "basics": '''{% set name = "World" %}
Hello, {{ name }}!

{% if user %}
    <p>Welcome, {{ user.name }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}''',
        "filters": '''{{ name | upper }}
{{ value | default("N/A") }}
{{ items | join(", ") }}''',
    },
    "tree": {
        "basics": '''.
├── src
│   ├── main.py
│   └── utils.py
├── tests
│   └── test_main.py
└── README.md''',
    },
    "powershell": {
        "basics": '''# Variables
$name = "World"
$count = 10

# Function
function Greet {
    param([string]$Name)
    Write-Host "Hello, $Name!"
}

# Conditionals
if ($name -eq "World") {
    Write-Host "Hello World"
} elseif ($name -eq "") {
    Write-Host "No name"
} else {
    Write-Host "Hello $name"
}

# Loops
foreach ($i in 1..$count) {
    Write-Host "Iteration $i"
}

# Arrays
$items = @("one", "two", "three")
Write-Host $items[0]''',
    },
    "plaintext": {
        "basics": '''This is a plain text file.

It contains no special formatting or syntax highlighting.

Lines can be of any length and contain any characters.

Numbers: 123, 456.789
Symbols: !@#$%^&*()
Special: <tag> [bracket] {brace} (paren)''',
    },
    "cuda": {
        "basics": '''__global__ void addKernel(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, n * sizeof(float));
    cudaMalloc(&d_b, n * sizeof(float));
    cudaMalloc(&d_c, n * sizeof(float));
    
    addKernel<<<blocks, threads>>>(d_a, d_b, d_c, n);
    cudaDeviceSynchronize();
    
    return 0;
}''',
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
    "dockerfile": ".dockerfile",
    "graphql": ".graphql",
    "hcl": ".tf",
    "groovy": ".groovy",
    "ini": ".ini",
    "csv": ".csv",
    "diff": ".diff",
    "makefile": ".makefile",
    "nginx": ".nginx",
    "pkl": ".pkl",
    "cue": ".cue",
    "protobuf": ".proto",
    "triton": ".triton",
    "stan": ".stan",
    "jinja": ".jinja",
    "tree": ".tree",
    "powershell": ".ps1",
    "plaintext": ".txt",
    "cuda": ".cu",
    "gleam": ".gleam",
    "groovy": ".groovy",
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

