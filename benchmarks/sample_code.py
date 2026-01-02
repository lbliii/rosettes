"""Sample code snippets for benchmarking."""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Python samples
# -----------------------------------------------------------------------------

PYTHON_SIMPLE = '''def hello():
    print("Hello, World!")
'''

PYTHON_MEDIUM = '''
import os
from pathlib import Path
from typing import Any

class FileHandler:
    """A class for handling file operations."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self._cache: dict[str, Any] = {}

    def read(self) -> str:
        """Read file contents."""
        if str(self.path) in self._cache:
            return self._cache[str(self.path)]

        with open(self.path) as f:
            content = f.read()

        self._cache[str(self.path)] = content
        return content

    def write(self, content: str) -> int:
        """Write content to file."""
        with open(self.path, "w") as f:
            return f.write(content)

    @property
    def exists(self) -> bool:
        return self.path.exists()


def process_files(directory: str) -> list[str]:
    """Process all files in a directory."""
    results = []
    for item in Path(directory).iterdir():
        if item.is_file():
            handler = FileHandler(str(item))
            results.append(handler.read())
    return results


if __name__ == "__main__":
    files = process_files(".")
    print(f"Processed {len(files)} files")
'''

# -----------------------------------------------------------------------------
# Rust sample
# -----------------------------------------------------------------------------

RUST_CODE = '''
use std::collections::HashMap;
use std::io::{self, Read, Write};

#[derive(Debug, Clone)]
pub struct Cache<K, V> {
    data: HashMap<K, V>,
    capacity: usize,
}

impl<K: Eq + std::hash::Hash, V: Clone> Cache<K, V> {
    pub fn new(capacity: usize) -> Self {
        Self {
            data: HashMap::with_capacity(capacity),
            capacity,
        }
    }

    pub fn get(&self, key: &K) -> Option<&V> {
        self.data.get(key)
    }

    pub fn insert(&mut self, key: K, value: V) -> Option<V> {
        if self.data.len() >= self.capacity {
            if let Some(first_key) = self.data.keys().next().cloned() {
                self.data.remove(&first_key);
            }
        }
        self.data.insert(key, value)
    }
}

fn main() -> io::Result<()> {
    let mut cache = Cache::new(100);
    cache.insert("key1".to_string(), 42);

    if let Some(val) = cache.get(&"key1".to_string()) {
        println!("Value: {}", val);
    }

    Ok(())
}
'''

# -----------------------------------------------------------------------------
# JavaScript/TypeScript sample
# -----------------------------------------------------------------------------

JAVASCRIPT_CODE = '''
import { useState, useEffect, useCallback } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

export function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/users');

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      setUsers(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, loading, error, refetch: fetchUsers };
}

export default function UserList() {
  const { users, loading, error } = useUsers();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
'''

# -----------------------------------------------------------------------------
# Go sample
# -----------------------------------------------------------------------------

GO_CODE = '''
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "sync"
)

type Cache struct {
    mu   sync.RWMutex
    data map[string]interface{}
}

func NewCache() *Cache {
    return &Cache{
        data: make(map[string]interface{}),
    }
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

func (c *Cache) Set(key string, value interface{}) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}

func main() {
    cache := NewCache()
    cache.Set("hello", "world")

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        val, _ := cache.Get("hello")
        json.NewEncoder(w).Encode(map[string]interface{}{
            "value": val,
        })
    })

    fmt.Println("Server starting on :8080")
    http.ListenAndServe(":8080", nil)
}
'''

# -----------------------------------------------------------------------------
# Scaled samples
# -----------------------------------------------------------------------------

PYTHON_LARGE = PYTHON_MEDIUM * 10  # ~500 lines


def generate_python_code(lines: int) -> str:
    """Generate synthetic Python code for benchmarking.

    Args:
        lines: Approximate number of lines to generate.

    Returns:
        Generated Python source code.
    """
    parts = [
        '"""Synthetic Python code for benchmarking."""',
        "",
        "import os",
        "import sys",
        "from pathlib import Path",
        "",
    ]

    for i in range(lines):
        if i % 10 == 0:
            parts.append(f"\n\nclass Class{i}:")
            parts.append(f'    """Docstring for Class{i}."""')
            parts.append("")
        elif i % 5 == 0:
            parts.append(f"    def method_{i}(self, arg1: str, arg2: int = 42) -> bool:")
            parts.append('        """Method docstring."""')
            parts.append("        # This is a comment")
            parts.append('        result = f"Value: {arg1}, {arg2}"')
            parts.append("        return len(result) > 0")
        else:
            parts.append(f"        x_{i} = {i} + 0x{i:04x} + 0b{i % 256:08b}")

    return "\n".join(parts)


# Pre-generated large samples
PYTHON_10K = generate_python_code(10_000)

