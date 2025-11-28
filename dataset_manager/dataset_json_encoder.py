from json import JSONEncoder
import datetime


from utils.logging import decorate_class_with_logging, DEBUG

@decorate_class_with_logging(log_level=DEBUG)
class DataSetJSONEncoder(JSONEncoder):
    """
    JSON encoder for `DataSet` objects and related dataclasses.

    This encoder provides two custom behaviours:

    - ``datetime.datetime`` instances are serialised to a compact string
      representation using the format ``"%Y.%m.%d_%H.%M.%S"``. This matches
      the format expected by `DataSet` and the corresponding JSON decoder.
    - All other objects are serialised via their ``__dict__`` attribute,
      which is sufficient for simple container-like classes such as `DataSet`.

    The encoder is intended to be used together with `DataSetJSONEncoder` to
    provide a round-trip-safe JSON representation of datasets.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y.%m.%d_%H.%M.%S")
        else:
            return o.__dict__
