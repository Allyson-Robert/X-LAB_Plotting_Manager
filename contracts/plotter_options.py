from utils.logging import DEBUG_PLOTTER, decorate_class_with_logging

@decorate_class_with_logging(log_level=DEBUG_PLOTTER)
class PlotterOptions:
    """
    Small, dictionary-backed container for named plotter options.

    Overview:
        Stores arbitrary named options, offers safe retrieval and `as_kwargs`
        filtering for passing options as **kwargs.

    - Supports add_option, get_option, has_options, as_kwargs.
    - Raises clear exceptions for missing keys or bad argument types.

    Usage Notes:
        Use as a simple options bag shared between workers and plotters.
    """
    def __init__(self):
        self.options = {}

    def add_option(self, label: str, value) -> bool:
        """ Add option if it does not already exist, if it does and the values conflict raise KeyError """
        if not self.has_options(label):
            self.options[label] = value
        elif self.get_option(label) != value:
            raise KeyError(f"Option with label {label} already exists in PlotterOptions")
        return True

    def update_option(self, label: str, value) -> bool:
        """ Update option if it exists, if not set option by calling add_option """
        if self.has_options(label):
            self.options[label] = value
        else:
            self.add_option(label, value)
        return True

    # Return option
    def get_option(self, label: str):
        # Check option existance before returning
        if self.has_options(label):
            return self.options[label]
        else:
            return None

    # Check whether the option exists
    def has_options(self, options_to_check):
        # Single option will typically be a string, put in list to be handled below
        if isinstance(options_to_check, str):
            options_to_check = [options_to_check]

        # Check if a list was passed
        if isinstance(options_to_check, list):
            # Verify that all listed options are present in the keys, return false for first missing option
            for option in options_to_check:
                if option not in self.options.keys():
                    return False
            return True
        # Fail if options_to_check is neither list not string
        else:
            raise ValueError(f"Passed incorrect type to PlotterOptions class, {type(options_to_check)} of {options_to_check} is not list or string")

    def __str__(self):
        return_string = ''
        for key in self.options.keys():
            return_string += f"{key}: {self.options[key]} "
        return return_string

    def as_kwargs(self, keys=None) -> dict:
        """
        Return a dict of options that can be passed as **kwargs.
        """

        # No filtering: return everything
        if keys is None:
            return dict(self.options)

        # Normalise single string to list
        if isinstance(keys, str):
            keys = [keys]

        # Sanity check
        try:
            iter(keys)
        except TypeError:
            raise TypeError("keys must be None, a string, or an iterable of strings")

        # Check all keys
        missing = [k for k in keys if k not in self.options]
        if missing:
            raise KeyError(f"Requested options not present: {missing}")

        # Return kwarg dict
        return {k: self.options[k] for k in keys}
