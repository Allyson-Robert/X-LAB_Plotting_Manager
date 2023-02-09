from data.collections.scatter_collections.scatter_collection import ScatterCollection
from data.data_processors.iv_data_processor import IVScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData


class IVScatterCollection(ScatterCollection):
    def __init__(self, collection_dict: dict[str, IVScatterDataProcessor]):
        self.collection = self.read_data(collection_dict)

    def read_data(self, collection_dict: dict) -> dict[str, IVScatterDataProcessor]:
        collection = {}
        for key in collection_dict:
            iv_data = IVScatterData(key)
            iv_data.read_file(collection_dict[key])
            collection[key] = IVScatterDataProcessor(iv_data)
        return collection

    def get_data(self) -> dict[str, IVScatterDataProcessor]:
        if self.collection is None:
            raise ValueError("Cannot get data before reading. Call read_data first")
        return self.collection
