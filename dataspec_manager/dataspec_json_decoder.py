from dataspec_manager import DataSpec
from json import JSONDecoder
import traceback


class DataSpecJSONDecoder(JSONDecoder):
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
