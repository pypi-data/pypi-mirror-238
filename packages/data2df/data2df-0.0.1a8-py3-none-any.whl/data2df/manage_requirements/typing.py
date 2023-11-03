from typing import TypeVar

PandasDataFrame = TypeVar("pandas.DataFrame")
PySparkDataFrame = TypeVar("pyspark.sql.DataFrame")
DaskDataFrame = TypeVar("dask.dataframe.DataFrame")
PolarsDataFrame = TypeVar("polars.DataFrame")
GeoPandasDataFrame = TypeVar("geopandas.GeoDataFrame")
GeoDaskDataFrame = TypeVar("dask_geopandas.GeoDataFrame")

SparkSession = TypeVar("pyspark.sql.SparkSession")
