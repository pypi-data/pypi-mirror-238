from .base import GeospatialDevice
from ..manage_requirements import (
    require_package,
    PandasDataFrame,
    DaskDataFrame,
    PySparkDataFrame,
    PolarsDataFrame,
    GeoPandasDataFrame,
    GeoDaskDataFrame,
    SparkSession,
)

from ..manage_requirements import GeoPandasDataFrame, SparkSession, require_package

from pathlib import Path

class GeoJSON(GeospatialDevice):
    def __init__(
        self,
        path,
        spark_session: SparkSession = None,
        spark_params: dict = {},
        push_pandas_kwargs: dict = {},
        to_pandas_kwargs: dict = {},
        push_dask_kwargs: dict = {},
        to_dask_kwargs: dict = {},
        push_pyspark_kwargs: dict = {},
        to_pyspark_kwargs: dict = {},
        push_polars_kwargs: dict = {},
        to_polars_kwargs: dict = {},
    ):
        """
        :param path: Location of the GeoJSON file
        """
        self.path = Path(path)
        super().__init__(
            spark_session=spark_session,
            spark_params=spark_params,
            push_pandas_kwargs=push_pandas_kwargs,
            to_pandas_kwargs=to_pandas_kwargs,
            push_dask_kwargs=push_dask_kwargs,
            to_dask_kwargs=to_dask_kwargs,
            push_pyspark_kwargs=push_pyspark_kwargs,
            to_pyspark_kwargs=to_pyspark_kwargs,
            push_polars_kwargs=push_polars_kwargs,
            to_polars_kwargs=to_polars_kwargs,
        )


    @require_package("geopandas")
    def push_pandas(self, data: GeoPandasDataFrame) -> None:
        # Semi-hack, to ensure compatibility with pandas
        # But you shouldn't pass pandas df to this
        data = geopandas.GeoDataFrame(data).set_geometry(
            [None for i in range(len(data))]
        )
        data.to_file(self.path, driver="GeoJSON")

    @require_package("geopandas")
    def to_pandas(self) -> GeoPandasDataFrame:
        data = geopandas.read_file(self.path)
        return data

    @require_package("dask-geopandas")
    def to_dask(self) -> GeoPandasDataFrame:
        raise NotImplementedError

    @require_package("dask-geopandas")
    def push_dask(self, data: GeoPandasDataFrame):
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
