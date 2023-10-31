from .base import BaseDevice
from .manage_requirements import (
    require_package,
    PandasDataFrame,
    DaskDataFrame,
    PySparkDataFrame,
    PolarsDataFrame,
)


class CSV(BaseDevice):
    def __init__(
        self,
        path: str,
        to_pandas_kwargs: dict = {},
        push_pandas_kwargs: dict = {},
    ):
        """
        :param path: Location of the CSV file or file-like object
        """
        self.path = path
        self.to_pandas_kwargs = to_pandas_kwargs
        self.push_pandas_kwargs = push_pandas_kwargs
        super().__init__()

    @require_package("pandas")
    def push_pandas(self, data: PandasDataFrame) -> None:
        data.to_csv(self.path, **(self.push_pandas_kwargs))

    @require_package("pandas")
    def to_pandas(self) -> PandasDataFrame:
        data = pandas.read_csv(self.path, **(self.to_pandas_kwargs))  # noqa: F821
        return data

    @require_package("dask")
    def to_dask(self) -> DaskDataFrame:
        raise NotImplementedError

    @require_package("dask")
    def push_dask(self, data: DaskDataFrame):
        raise NotImplementedError

    @require_package("pyspark")
    def to_pyspark(self) -> PySparkDataFrame:
        raise NotImplementedError

    @require_package("pyspark")
    def push_pyspark(self, data: PySparkDataFrame):
        raise NotImplementedError

    @require_package("polars")
    def to_polars(self) -> PolarsDataFrame:
        raise NotImplementedError

    @require_package("polars")
    def push_polars(self, data: PolarsDataFrame):
        raise NotImplementedError

    def _check_validity(self) -> bool:
        raise NotImplementedError
