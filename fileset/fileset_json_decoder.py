from fileset import Fileset
from json import JSONDecoder


class FilesetJSONDecoder(JSONDecoder):
    def __init__(self, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        super().__init__(**kwargs)

    @staticmethod
    def object_hook(dct):
        try:
            fileset = Fileset(dct['date'])
            fileset.set_name(dct['name'])
            fileset.set_device(dct['device'])
            fileset.set_notes(dct['notes'])
            fileset.set_console(dct['console'])
            fileset.set_filepaths(dct['filepaths'])

            return fileset

        except KeyError:
            return dct
