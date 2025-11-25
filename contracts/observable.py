"""
Observable contract used by DataCore and DataProcessorCore.

Defines the canonical structure for observable entries stored in
`raw_data` and `processed_data` mappings throughout the X-LAB plotting
ecosystem.

An Observable bundles a payload together with its display units:

- ``units``: Human-readable unit string, or ``None`` for unitless data.
- ``data``: The underlying payload (e.g. list, array, scalar, etc.).
"""

from typing import TypedDict, Any

# Contract for items to use in data dictionaries
class Observable(TypedDict):
    units: str | None
    data: Any
