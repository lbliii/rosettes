"""Pytest configuration for benchmarks."""

from __future__ import annotations


def pytest_configure(config):
    """Configure pytest for benchmark runs."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m not slow')")

