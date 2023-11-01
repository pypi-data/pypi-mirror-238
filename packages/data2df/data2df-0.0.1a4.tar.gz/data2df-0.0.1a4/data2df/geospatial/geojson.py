from . import GeospatialDevice
from ..manage_requirements import GeoDataFrame


class GeoJSON(GeospatialDevice):
    def __init__(self, path):
        # self._check_validity()
        self.path = path

    @require_package("geopandas")
    def push_pandas(self, data: GeoDataFrame) -> None:
        data.to_file(self.path, driver="GeoJSON")

    @require_package("geopandas")
    def to_pandas(self) -> GeoDataFrame:
        data = gpd.read_file(self.path)
        return data

    def to_dask(self) -> GeoDataFrame:
        raise NotImplementedError

    def push_dask(self, data: GeoDataFrame):
        raise NotImplementedError

    def _check_validity(self) -> bool:
        raise NotImplementedError
