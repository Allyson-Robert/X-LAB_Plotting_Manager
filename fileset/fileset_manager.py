import json
from fileset import Fileset
from fileset_json_encoder import FilesetJSONEncoder
from fileset_json_decoder import FilesetJSONDecoder


class FilesetManager:
    def __init__(self):
        pass

    @staticmethod
    def save_fileset(fileset, file_name):
        """ Saves the fileset data into a JSON file """
        assert isinstance(fileset, Fileset)

        # Who should check whether the filename is valid?
        with open(file_name, "w") as json_file:
            json.dump(fileset, json_file, cls=FilesetJSONEncoder)
        json_file.close()

    @staticmethod
    def open_fileset(file_name):
        with open(file_name) as json_file:
            return json.load(json_file, cls=FilesetJSONDecoder)
