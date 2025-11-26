from dataspec_manager import DataSpec
from json import JSONDecoder
from utils.logging import decorate_class_with_logging, DEBUG


@decorate_class_with_logging(log_level=DEBUG)
class DataSpecJSONDecoder(JSONDecoder):
    """
    Custom JSON decoder that reconstructs `DataSpec` instances from JSON.

    This decoder installs an `object_hook` that:
    - Detects dictionaries carrying the expected `DataSpec` fields
      (e.g. ``creation_date``, ``name``, ``device``, ``experiment_date_time``,
      ``notes``, ``console``, ``structure_type``, ``filepaths``, ``colours``).
    - Instantiates a new `DataSpec` using the stored creation date.
    - Replays all relevant setters to restore metadata, structure type, paths,
      colours, and annotations.

    If a JSON object does not match the expected shape, it is returned unchanged,
    allowing non-`DataSpec` data to be decoded normally.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def object_hook(dct):
        try:
            dataspec = DataSpec(dct['creation_date'])
            dataspec.set_name(dct['name'])
            dataspec.set_device(dct['device'])
            dataspec.set_experiment_date(dct['experiment_date_time'])
            dataspec.set_notes(dct['notes'])
            dataspec.set_console(dct['console'])
            dataspec.set_structure_type(dct['structure_type'])
            dataspec.set_filepaths(dct['filepaths'])
            dataspec.set_colours(dct['colours'])

            return dataspec

        except KeyError:
            return dct
