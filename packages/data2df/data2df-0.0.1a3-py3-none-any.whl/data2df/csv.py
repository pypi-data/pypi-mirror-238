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
        push_pandas_kwargs: dict = {},
        to_pandas_kwargs: dict = {},
        push_dask_kwargs: dict = {},
        to_dask_kwargs: dict = {},
        push_pyspark_kwargs: dict = {},
        to_pyspark_kwargs: dict = {},
        push_polars_kwargs: dict = {},
        to_polars_kwargs: dict = {}
    ):
        """
        :param path: Location of the CSV file or file-like object
        """
        self.path = path
        super().__init__(
            push_pandas_kwargs=push_pandas_kwargs,
            to_pandas_kwargs=to_pandas_kwargs,
            push_dask_kwargs=push_dask_kwargs,
            to_dask_kwargs=to_dask_kwargs,
            push_pyspark_kwargs=push_pyspark_kwargs,
            to_pyspark_kwargs=to_pyspark_kwargs,
            push_polars_kwargs=push_polars_kwargs,
            to_polars_kwargs=to_polars_kwargs
        )

    @require_package("pandas")
    def push_pandas(self, data: PandasDataFrame) -> None:
        data.to_csv(self.path, **(self.push_pandas_kwargs))

    @require_package("pandas")
    def to_pandas(self) -> PandasDataFrame:
        data = pandas.read_csv( # noqa: F821
            self.path,
            **(self.to_pandas_kwargs)
        )  
        return data

    @require_package("dask")
    def push_dask(self, data: DaskDataFrame):
        data.to_csv(
            [self.path],
            **(self.push_dask_kwargs)
        )

    @require_package("dask")
    def to_dask(self) -> DaskDataFrame:
        data = dask.dataframe.read_csv( # noqa: F821
            self.path,
            **(self.to_dask_kwargs)
        )
        return data

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
