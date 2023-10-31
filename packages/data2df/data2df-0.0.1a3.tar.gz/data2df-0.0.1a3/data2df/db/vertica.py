from .base import DBTable
from ..manage_requirements import DaskDataFrame


class VerticaTable(DBTable):
    """
    This class reads and writes from Vertica using sqlalchemy.
    This is not efficient for large data, it should be rewritten using verticapy
    """

    def __init__(
        self,
        table: str,
        host: str,
        user: str,
        password: str,
        database: str,
        schema: str,
        port: int = 5433,
        push_pandas_kwargs: dict = {},
        to_pandas_kwargs: dict = {},
        push_dask_kwargs: dict = {},
        to_dask_kwargs: dict = {},
        push_pyspark_kwargs: dict = {},
        to_pyspark_kwargs: dict = {},
        push_polars_kwargs: dict = {},
        to_polars_kwargs: dict = {}
    ):
        super().__init__(
            table,
            host,
            port,
            user,
            password,
            database,
            schema,
            "vertica+vertica_python",
            push_pandas_kwargs=push_pandas_kwargs,
            to_pandas_kwargs=to_pandas_kwargs,
            push_dask_kwargs=push_dask_kwargs,
            to_dask_kwargs=to_dask_kwargs,
            push_pyspark_kwargs=push_pyspark_kwargs,
            to_pyspark_kwargs=to_pyspark_kwargs,
            push_polars_kwargs=push_polars_kwargs,
            to_polars_kwargs=to_polars_kwargs
        )
