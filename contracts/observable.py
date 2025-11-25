from typing import TypedDict, Any

# Contract for items to use in data dictionaries
class Observable(TypedDict):
    units: str
    data: Any
