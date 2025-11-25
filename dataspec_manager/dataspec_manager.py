import json
from dataspec_manager import DataSpec
from dataspec_json_encoder import DataSpecJSONEncoder
from dataspec_json_decoder import DataSpecJSONDecoder


class DataSpecManager:
    """
       Small helper class for persisting `DataSpec` instances to and from JSON files.

       Responsibilities
       ----------------
       - `save_dataspec(dataspec, file_name)`:
           Serialises a `DataSpec` instance to disk using `DataSpecJSONEncoder`.
           The method asserts that the passed object is a `DataSpec` and writes
           the encoded JSON to the given file path.
       - `open_dataspec(file_name)`:
           Opens a JSON file and deserialises it into a `DataSpec` instance using
           `DataSpecJSONDecoder`.

       The manager does not interpret the dataspec content; it only handles the
       IO and wiring between JSON encoder/decoder and the underlying `DataSpec`
       objects.
   """
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
