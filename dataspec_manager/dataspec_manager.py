import json
from dataspec_manager import DataSpec
from dataspec_json_encoder import DataSpecJSONEncoder
from dataspec_json_decoder import DataSpecJSONDecoder


class DataSpecManager:
    def __init__(self):
        pass

    @staticmethod
    def save_dataspec(dataspec, file_name):
        """ Saves the dataspec_manager data into a JSON file """
        assert isinstance(dataspec, DataSpec)

        # Who should check whether the filename is valid?
        with open(file_name, "w") as json_file:
            json.dump(dataspec, json_file, cls=DataSpecJSONEncoder)
        json_file.close()

    @staticmethod
    def open_dataspec(file_name):
        with open(file_name) as json_file:
            return json.load(json_file, cls=DataSpecJSONDecoder)
