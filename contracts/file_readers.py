"""
File reader contracts for use by DataCore and DataProcessingCore.

Defines the canonical function signature and return type used by all
file readers in the X-LAB plotting ecosystem.

A *file reader* is any callable matching `FileReaderFn`:
    (path: str) -> ReaderOutput

Responsibilities:
    - Open and parse a file at the given path.
    - Return structured raw data as a mapping of semantic keys
      (e.g. "x_axis", "y_axis", "current", "meta") to Python objects.
    - Perform no higher-level processing or conversion to observables.
"""

from typing import Any, Mapping, Callable, TypeAlias

# Every reader returns a mapping from string keys to "data blobs"
# A blob can be: list/array, dict, scalar, whatever the Data class expects.
ReaderOutput: TypeAlias = Mapping[str, Any]

# Contract for reader functions
FileReaderFn: TypeAlias = Callable[[str], ReaderOutput]