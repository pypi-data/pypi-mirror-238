from ..base import BaseDevice
from ..manage_requirements import (
    require_package,
    PandasDataFrame,
    DaskDataFrame,
    PySparkDataFrame,
    PolarsDataFrame,
)


class DBTable(BaseDevice):
    @require_package("sqlalchemy")
    def __init__(
        self,
        table: str,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        schema: str,
        driver: str,
        push_pandas_kwargs: str = {},
        to_pandas_kwargs: str = {},
    ):
        self.table = table
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.driver = driver
        self.connection_url = f"{driver}://{user}:{password}@{host}:{port}/{database}"
        self.push_pandas_kwargs = push_pandas_kwargs
        self.to_pandas_kwargs = to_pandas_kwargs

    @require_package("pandas")
    def push_pandas(
        self, data: PandasDataFrame, if_exists="replace", index=False
    ) -> None:
        data.to_sql(
            name=self.table,
            schema=self.schema,
            con=self._get_engine(),
            dtype=self._update_type(data),
            **(self.push_pandas_kwargs),
        )

    @require_package("pandas")
    def to_pandas(self) -> PandasDataFrame:
        data = pandas.read_sql_table(
            table_name=self.table,
            schema=self.schema,
            con=self._get_engine(),
            **(self.to_pandas_kwargs),
        )
        return data

    def _get_engine(self):
        engine = sqlalchemy.create_engine(self.connection_url)
        return engine

    def _update_type(self, df):
        dtypedict = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                max_len = df[i].str.len().max()
                dtypedict.update({i: sqlalchemy.types.VARCHAR(max_len + 1)})

        return dtypedict

    @require_package("dask")
    def to_dask(self) -> DaskDataFrame:
        raise NotImplementedError

    @require_package("dask")
    def push_dask(self, data: DaskDataFrame):
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

    def _check_validity(self):
        pass

    @classmethod
    def from_query(self):
        """
        The idea is: launch a query, put the result into schema.table (maybe?)
        and return the device
        """
        raise NotImplementedError
