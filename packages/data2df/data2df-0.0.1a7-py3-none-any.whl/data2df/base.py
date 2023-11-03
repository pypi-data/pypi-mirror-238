from abc import ABC, abstractmethod
from .manage_requirements import (
    require_package,
    PandasDataFrame,
    DaskDataFrame,
    PySparkDataFrame,
    PolarsDataFrame,
    SparkSession,
)


class BaseDevice(ABC):
    """
    Defines the basic properties needed for any I/O device
    In this context we only consider devices that can contain tabular data
    (DB tables, CSV, ...).
    It might make sense to extend the class to e.g. JSON, conf files.
    I would rather keep that kind of I/O in the utils functions.

    Only supports Pandas and Dask for now, would be nice to extend to Polars.

    """

    def __init__(
        self,
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
        self.spark_session = spark_session
        self.spark_params = spark_params  # or self._spark_defaults
        self.push_pandas_kwargs = push_pandas_kwargs
        self.to_pandas_kwargs = to_pandas_kwargs
        self.push_dask_kwargs = push_dask_kwargs
        self.to_dask_kwargs = to_dask_kwargs
        self.push_pyspark_kwargs = push_pyspark_kwargs
        self.to_pyspark_kwargs = to_pyspark_kwargs
        self.push_polars_kwargs = push_polars_kwargs
        self.to_polars_kwargs = to_polars_kwargs

    @abstractmethod
    def push_pandas(self, data: PandasDataFrame) -> None:
        pass

    @abstractmethod
    def to_pandas(self) -> PandasDataFrame:
        pass

    @abstractmethod
    def to_dask(self) -> DaskDataFrame:
        pass

    @abstractmethod
    def push_dask(self, data: DaskDataFrame):
        pass

    @abstractmethod
    def to_pyspark(self) -> PySparkDataFrame:
        pass

    @abstractmethod
    def push_pyspark(self, data: PySparkDataFrame):
        pass

    @abstractmethod
    def to_polars(self) -> PolarsDataFrame:
        pass

    @abstractmethod
    def push_polars(self, data: PolarsDataFrame):
        pass

    @abstractmethod
    def _check_validity(self) -> bool:
        pass

    @require_package("pyspark")
    def _get_or_create_spark_session(self) -> SparkSession:
        if self.spark_session is None:
            builder = pyspark.sql.SparkSession.builder.appName("data2df_instance")
            for key, value in self.spark_params.items():
                builder = builder.config(key, item)
            spark = builder.getOrCreate()

            # If pyspark >= 3.4
            #spark = (
            #    pyspark.sql.SparkSession.builder.appName("data2df_instance")
            #    .config(map=self.spark_params)
            #    .getOrCreate()
            #)

            self.spark_session = spark

        return self.spark_session

    _spark_defaults = {
        "spark.executor.memory": 5,
        "spark.executor.cores": 8,
        "spark.driver.memory": 5,
        "spark.driver.maxResultSize": 10,
        #'spark.local.dir', './.sparkTmp'
    }
