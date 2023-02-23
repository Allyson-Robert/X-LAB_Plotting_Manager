def get_class_methods(cls, ignore=[]) -> list:
    methods = []
    # Get all class attributes from __dict__
    for attribute in cls.__dict__:
        # Add callable attributes that aren't 1) dunders 2) private methods
        if callable(getattr(cls, attribute)) and not attribute.startswith('_'):
            # Ignore setters and explicitly mentioned methods
            if not attribute.startswith('set') and attribute not in ignore:
                methods.append(attribute)

    return methods
