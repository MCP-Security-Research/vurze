"""Tests for the 'pyseal decorate' CLI command."""

import os
import subprocess
import tempfile
import pytest

SAMPLE_CODE = """
def foo():
    return 42

class Bar:
    def baz(self):
        return 'baz'
"""

EMPTY_CODE = """
# No functions or classes here
x = 123
"""

def test_decorate_injects_decorators():
    """Test that 'pyseal decorate' injects decorators into all functions and classes in a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "sample.py")
        with open(file_path, "w") as f:
            f.write(SAMPLE_CODE)
        result = subprocess.run(["pyseal", "decorate", file_path], capture_output=True, text=True)
        assert result.returncode == 0, f"pyseal decorate failed: {result.stderr}"
        with open(file_path) as f:
            content = f.read()
        assert any(line.strip().startswith("@pyseal._") for line in content.splitlines()), "Decorator not injected into file"

def test_decorate_idempotency():
    """Test that running 'pyseal decorate' twice does not duplicate decorators."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "sample.py")
        with open(file_path, "w") as f:
            f.write(SAMPLE_CODE)
        subprocess.run(["pyseal", "decorate", file_path], capture_output=True, text=True)
        # Run again
        result = subprocess.run(["pyseal", "decorate", file_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Second pyseal decorate failed: {result.stderr}"
        with open(file_path) as f:
            content = f.read()
        # Should only have one decorator per function/class
        decorator_lines = [line for line in content.splitlines() if line.strip().startswith("@pyseal._")]
        assert len(decorator_lines) == 2, "Duplicate or missing decorators found"

def test_decorate_handles_empty_file():
    """Test that 'pyseal decorate' handles files with no functions/classes gracefully."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "empty.py")
        with open(file_path, "w") as f:
            f.write(EMPTY_CODE)
        result = subprocess.run(["pyseal", "decorate", file_path], capture_output=True, text=True)
        assert result.returncode == 0, f"pyseal decorate failed on empty file: {result.stderr}"
        with open(file_path) as f:
            content = f.read()
        assert "@pyseal_decorator" not in content, "Decorator should not be injected into empty file"
