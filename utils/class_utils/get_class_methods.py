from types import FunctionType


def get_class_methods(cls, ignore=[]) -> list:
    """
    Return the names of public methods defined directly on a class.

    Parameters
    ----------
    cls:
        Class whose methods should be inspected.
    ignore:
        Optional list of method names to exclude from the result.

    Returns
    -------
    list[str]
        Names of methods defined on ``cls`` that are:
        - plain functions (no descriptors),
        - not dunder methods,
        - not starting with ``set``,
        - not listed in ``ignore``.
    """
    methods = []
    for name, func in cls.__dict__.items():
        # Skip items that are not of the function type
        if type(func) != FunctionType:
            continue
        # ignore dunder_methods, setters and explicitly ignored function names
        if not name.startswith('_') and not name.startswith('set') and name not in ignore:
            methods.append(name)

    return methods
