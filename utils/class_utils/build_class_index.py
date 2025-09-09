import pkgutil
import importlib
import inspect


def build_class_index(package_name: str):
    """
    Scan a package for class_utils definitions without importing all modules at once.
    Returns a dict mapping class_utils name to (module_name, class_name).
    """
    index = {}
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)  # minimal import to inspect
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                index[name] = (module_name, name)
    return index
