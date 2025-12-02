import json
from dataset_manager import DataSet
from dataset_json_encoder import DataSetJSONEncoder
from dataset_json_decoder import DataSetJSONDecoder
from utils.logging import decorate_class_with_logging, DEBUG

@decorate_class_with_logging(log_level=DEBUG)
class DataSetManager:
    """
       Small helper class for persisting `DataSet` instances to and from JSON files.

       Responsibilities
       ----------------
       - `save_dataset(dataset, file_name)`:
           Serialises a `DataSet` instance to disk using `DataSetJSONEncoder`.
           The method checks that the passed object is a `DataSet` and writes
           the encoded JSON to the given file path.
       - `open_dataset(file_name)`:
           Opens a JSON file and deserialises it into a `DataSet` instance using
           `DataSetJSONDecoder`.

       The manager does not interpret the dataset content; it only handles the
       IO and wiring between JSON encoder/decoder and the underlying `DataSet`
       objects.
   """
    def __init__(self):
        pass

    @staticmethod
    def save_dataset(dataset, file_name):
        """ Saves the dataset_manager data into a JSON file """
        if not isinstance(dataset, DataSet):
            raise ValueError("dataset must be an instance of DataSet")

        # Who should check whether the filename is valid?
        with open(file_name, "w") as json_file:
            json.dump(dataset, json_file, cls=DataSetJSONEncoder)
        json_file.close()

    @staticmethod
    def open_dataset(file_name):
        with open(file_name) as json_file:
            return json.load(json_file, cls=DataSetJSONDecoder)
