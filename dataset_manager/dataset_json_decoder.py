from dataset_manager import DataSet
from json import JSONDecoder
from utils.logging import decorate_class_with_logging, DEBUG


@decorate_class_with_logging(log_level=DEBUG)
class DataSetJSONEncoder(JSONDecoder):
    """
    Custom JSON decoder that reconstructs `DataSet` instances from JSON.

    This decoder installs an `object_hook` that:
    - Detects dictionaries carrying the expected `DataSet` fields
      (e.g. ``creation_date``, ``name``, ``device``, ``experiment_date_time``,
      ``notes``, ``console``, ``structure_type``, ``filepaths``, ``colours``).
    - Instantiates a new `DataSet` using the stored creation date.
    - Replays all relevant setters to restore metadata, structure type, paths,
      colours, and annotations.

    If a JSON object does not match the expected shape, it is returned unchanged,
    allowing non-`DataSet` data to be decoded normally.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def object_hook(dct):
        try:
            dataset = DataSet(dct['creation_date'])
            dataset.set_name(dct['name'])
            dataset.set_device(dct['device'])
            dataset.set_experiment_date(dct['experiment_date_time'])
            dataset.set_notes(dct['notes'])
            dataset.set_console(dct['console'])
            dataset.set_structure_type(dct['structure_type'])
            dataset.set_filepaths(dct['filepaths'])
            dataset.set_colours(dct['colours'])

            return dataset

        except KeyError:
            return dct
