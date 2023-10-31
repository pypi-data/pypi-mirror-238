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
        push_pandas_kwargs: str = {},
        to_pandas_kwargs: str = {},
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
            push_pandas_kwargs,
            to_pandas_kwargs,
        )
