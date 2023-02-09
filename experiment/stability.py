from fileset.fileset import Fileset
from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection


class Stability:
    def __init__(self):
        self.scatter_collection = None

    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "structured"
        self.scatter_collection = IVScatterCollection(fileset.get_filepaths())

