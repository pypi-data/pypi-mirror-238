from .base import DBTable


class PostgresTable(DBTable):
    def __init__(
        self,
        table: str,
        host: str,
        user: str,
        password: str,
        database: str,
        schema: str = None,
        port: int = 5432,
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
            "postgres",
            push_pandas_kwargs,
            to_pandas_kwargs,
        )
