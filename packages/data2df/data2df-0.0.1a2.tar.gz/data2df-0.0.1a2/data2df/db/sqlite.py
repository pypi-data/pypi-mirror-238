from .base import DBTable


class SQLiteTable(DBTable):
    def __init__(
        self,
        table: str,
        location: str = ":memory:",
        push_pandas_kwargs: str = {},
        to_pandas_kwargs: str = {},
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
            push_pandas_kwargs,
            to_pandas_kwargs,
        )
        self.table = table
        self.location = location
        self.connection_url = f"sqlite:///{location}"
