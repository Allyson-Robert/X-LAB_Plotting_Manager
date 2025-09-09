import importlib


def load_class_from_index(class_index, class_name: str):
    """
    Given a class_utils index (from build_class_index) and a class_utils name,
    import and return the class_utils object.
    """
    if class_name not in class_index:
        raise ValueError(f"Class '{class_name}' not found.")

    module_name, cls_name = class_index[class_name]
    module = importlib.import_module(module_name)
    return getattr(module, cls_name)
