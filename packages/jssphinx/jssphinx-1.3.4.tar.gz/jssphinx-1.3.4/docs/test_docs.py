import logging
from pathlib import Path

import pytest
from faker_file.registry import FILE_REGISTRY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "execute_file",
    "test_dynamic_files",
)

# Walk through the directory and all subdirectories for .py files
example_dir = Path("docs/_static/py")
py_files = sorted([str(p) for p in example_dir.rglob("*.py")])


def execute_file(file_path, caplog):
    """Dynamic test function."""
    global_vars = {}
    # Set the log level to WARNING for this block
    with caplog.at_level(logging.WARNING):
        with open(file_path, "r") as f:
            code = f.read()
        exec(code, global_vars)


@pytest.mark.parametrize("file_path", py_files)
def test_dynamic_files(file_path, caplog):
    execute_file(file_path, caplog)
    FILE_REGISTRY.clean_up()
