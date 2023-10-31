from abc import ABC, abstractmethod
from .manage_requirements import (
    require_package,
    PandasDataFrame,
    DaskDataFrame,
    PySparkDataFrame,
    PolarsDataFrame,
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

    def __init__(self):
        # https://stackoverflow.com/questions/50384862/python-metaprogramming-generate-a-function-signature-with-type-annotation
        # When class is instantiated, change type annotations of functions based on available packages
        # Does it make sense to do it?
        pass

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
