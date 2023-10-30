from ..base import BaseDevice
from ..manage_requirements import require_package, PandasDataFrame, DaskDataFrame

class DBTable(BaseDevice):
    def __init__(
        self,
        table: str,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        schema: str
    ):
        self.table = table
        self.host = host 
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema

    @require_package('pandas')
    @require_package('sqlalchemy')
    def push_pandas(self, data: PandasDataFrame, if_exists='replace', index=False) -> None:
        data.to_sql(
            name = self.table, 
            schema = self.schema,
            con = self._get_engine(),
            if_exists=if_exists, 
            index=index,
            dtype=self._update_type(data)
        )
    
    @require_package('pandas') 
    @require_package('sqlalchemy')
    def to_pandas(self) -> PandasDataFrame:
        data = pd.read_sql_table(
            table_name = self.table,
            schema = self.schema,
            con = self._get_engine()
        )
        return data
    
    def _get_engine(self):
        engine = sqlalchemy.create_engine(self.connection_url)
        return engine

    def _update_type(self, df):
        dtypedict = {}
        for i,j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                max_len = df[i].str.len().max()
                dtypedict.update({i: sqlalchemy.types.VARCHAR(max_len+1)})

        return dtypedict

    @classmethod
    def from_query(self):
        '''
        The idea is: launch a query, put the result into schema.table (maybe?)
        and return the device
        '''
        raise NotImplementedError




class PostgresTable(DBTable):
    def __init__(
        self,
        table: str,
        host: str,
        user: str,
        password: str,
        database: str,
        schema: str = None,
        port: int = 5432
    ):
        self.connection_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
        # TODO: use kwargs here
        super().__init__(table, host, port, user, password, database, schema)

    def to_dask(self) -> DaskDataFrame:
        raise NotImplementedError
    
    def push_dask(self, data: DaskDataFrame):
        raise NotImplementedError
    
    def _check_validity(self) -> bool:
        raise NotImplementedError


