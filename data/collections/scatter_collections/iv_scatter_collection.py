from data.datatypes.scatter_data.iv_scatter import IVScatterData
from data.collections.scatter_collections.scatter_collection import ScatterCollection


class IVScatterCollection(ScatterCollection):
    def __init__(self, collection_dict: dict):
        self.collection = self.read_data(collection_dict)

    def read_data(self, collection_dict: dict) -> dict:
        collection = {}
        for key in collection_dict:
            collection[key] = IVScatterData(key)
            collection[key].read_file(collection_dict[key])
        return collection

    def get_data(self) -> dict[str, IVScatterData]:
        if self.collection is None:
            raise ValueError("Cannot get data before reading. Call read_data first")
        return self.collection

