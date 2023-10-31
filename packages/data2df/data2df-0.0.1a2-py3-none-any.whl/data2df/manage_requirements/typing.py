from typing import TypeVar

PandasDataFrame = TypeVar("pd.DataFrame")
PySparkDataFrame = TypeVar("pyspark.sql.DataFrame")
DaskDataFrame = TypeVar("dask.dataframe.DataFrame")
PolarsDataFrame = TypeVar("polars.DataFrame")
