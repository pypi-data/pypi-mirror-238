from .base import DBTable


class SQLiteTable(DBTable):
    def __init__(
        self,
        table: str,
        location: str = ":memory:",
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
            None,
            None,
            None,
            None,
            None,
            None,
            "sqlite",
            push_pandas_kwargs=push_pandas_kwargs,
            to_pandas_kwargs=to_pandas_kwargs,
            push_dask_kwargs=push_dask_kwargs,
            to_dask_kwargs=to_dask_kwargs,
            push_pyspark_kwargs=push_pyspark_kwargs,
            to_pyspark_kwargs=to_pyspark_kwargs,
            push_polars_kwargs=push_polars_kwargs,
            to_polars_kwargs=to_polars_kwargs
        )
        self.table = table
        self.location = location
        self.connection_url = f"sqlite:///{location}"
