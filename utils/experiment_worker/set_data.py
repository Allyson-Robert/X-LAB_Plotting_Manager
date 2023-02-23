from typing import Type
from fileset.fileset import Fileset
from data.datatypes.scatter_data.scatter import ScatterData
from data.data_processors.scatter_data.data_processors import ScatterDataProcessor


def set_data(fileset: Fileset, scatter_data: Type[ScatterData], scatter_data_processor: Type[ScatterDataProcessor]) \
        -> dict[str, ScatterDataProcessor]:
    assert fileset.get_structure_type() == "flat"

    filepaths = fileset.get_filepaths()
    data_processors = {}
    for path in filepaths:
        data = scatter_data(path)
        data.read_file(filepaths[path])
        data_processors[path] = scatter_data_processor(data)

    return data_processors
