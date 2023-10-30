from . import BaseDevice
from .manage_requirements import PandasDataFrame, DaskDataFrame


class ParquetDir(BaseDevice):
    def __init__(self, path: str):
        """
        :param path: Location of the directory containing parquet data
        """

        self.path = path

        super().__init__()

    def push_pandas(self, data: PandasDataFrame) -> None:
        raise NotImplementedError

    def to_pandas(self) -> PandasDataFrame:
        raise NotImplementedError

    def to_dask(self) -> PandasDataFrame:
        data = dd.read_parquet(self.path)
        return data

    def push_dask(self, data: PandasDataFrame):
        raise NotImplementedError

    def _check_validity(self) -> bool:
        raise NotImplementedError
