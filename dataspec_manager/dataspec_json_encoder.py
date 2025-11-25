from json import JSONEncoder
import datetime


class DataSpecJSONEncoder(JSONEncoder):
    """
    JSON encoder for `DataSpec` objects and related dataclasses.

    This encoder provides two custom behaviours:

    - ``datetime.datetime`` instances are serialised to a compact string
      representation using the format ``"%Y.%m.%d_%H.%M.%S"``. This matches
      the format expected by `DataSpec` and the corresponding JSON decoder.
    - All other objects are serialised via their ``__dict__`` attribute,
      which is sufficient for simple container-like classes such as `DataSpec`.

    The encoder is intended to be used together with `DataSpecJSONDecoder` to
    provide a round-trip-safe JSON representation of dataspecs.
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y.%m.%d_%H.%M.%S")
        else:
            return o.__dict__
