class VocNotFoundError(ValueError):
    """Raised when an open-circuit voltage (Voc) value cannot be located."""
    pass


class IscNotFoundError(ValueError):
    """Raised when a short-circuit current (Isc) value cannot be located."""
    pass


class ObservableNotComputableError(ValueError):
    """Raised when a requested observable cannot be derived from the available data."""
    pass


class IncompatibleDeviceTypeFound(KeyError):
    """Raised when a dataspec or configuration refers to an unknown device type."""
    pass


class ImplementationError(RuntimeError):
    """Raised when the implementations package fails validation."""