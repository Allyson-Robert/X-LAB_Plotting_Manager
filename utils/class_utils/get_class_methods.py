import inspect


def get_class_methods(cls, ignore=[]) -> list:
    methods = []
    # Apparently there is a function to get the members from a class_utils
    for name, func in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_') and not name.startswith('set') and name not in ignore:
            methods.append(name)
    return methods
