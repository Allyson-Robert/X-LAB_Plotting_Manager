from dataset_manager import DataSet, DataSetJSONDecoder, DataSetJSONEncoder
import json


def create_fileset() -> DataSet:
    path = "G:\\My Drive\\Data\\Sunbrick\\2023\\01-January\\20_12_2022_Long-term_IV\\Position_1\\IV_2023_01_02_22_40_50.txt"
    label = "test curve"

    fs = DataSet("2023-02-09")
    fs.add_filepath(path, label)
    fs.set_name("Testing")
    fs.set_device("Sunbrick")

    return fs


def save_fileset(fileset: DataSet, path: str):
    with open(path, "w") as json_file:
        json.dump(fileset, json_file, cls=DataSetJSONDecoder)
    json_file.close()


def open_fileset(path: str) -> DataSet:
    with open(path) as json_file:
        fileset = json.load(json_file, cls=DataSetJSONEncoder)
    return fileset


path = "../test_json.json"
test_fs = create_fileset()
save_fileset(test_fs, path)
opened_fs = open_fileset(path)
