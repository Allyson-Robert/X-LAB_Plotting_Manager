from typing import Type
from fileset.fileset import Fileset
from data.datatypes.data import Data
from data.data_processors.data_processors import DataProcessor


def set_data(fileset: Fileset, scatter_data: Type[Data], scatter_data_processor: Type[DataProcessor]) \
        -> dict[str, DataProcessor]:
    assert fileset.get_structure_type() == "flat"

    filepaths = fileset.get_filepaths()
    data_processors = {}
    for path in filepaths:
        data = scatter_data(path)
        data.read_file(filepaths[path])
        data_processors[path] = scatter_data_processor(data)

    return data_processors
