def get_class_methods(cls):
    methods = []
    # Get all class attributes
    for attribute in dir(cls):
        # Add callable attributes that aren't dunders
        if callable(getattr(cls, attribute)) and not attribute.startswith('__'):
            # Ignore setters
            if not attribute.startswith('set'):
                methods.append(attribute)

    return methods
