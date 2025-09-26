from types import FunctionType


# Returns class methods from class.__items__() that are functions
def get_class_methods(cls, ignore=[]) -> list:
    methods = []
    for name, func in cls.__dict__.items():
        # Skip items that are not of the function type
        if type(func) != FunctionType:
            continue
        # ignore dunder_methods, setters and explicitly ignored function names
        if not name.startswith('_') and not name.startswith('set') and name not in ignore:
            methods.append(name)

    return methods
