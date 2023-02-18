from fileset import Fileset
from json import JSONDecoder
import traceback


class FilesetJSONDecoder(JSONDecoder):
    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def object_hook(dct):
        try:
            fileset = Fileset(dct['creation_date'], dct['experiment_date_time'])
            fileset.set_name(dct['name'])
            fileset.set_device(dct['device'])
            fileset.set_notes(dct['notes'])
            fileset.set_console(dct['console'])
            fileset.set_structure_type(dct['structure_type'])
            fileset.set_filepaths(dct['filepaths'])

            return fileset

        except KeyError:
            return dct
