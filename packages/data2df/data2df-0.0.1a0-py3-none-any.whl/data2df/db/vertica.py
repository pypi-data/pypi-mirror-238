from .base import DBTable
from ..manage_requirements import DaskDataFrame

class VerticaTable(DBTable):
    '''
    This class reads and writes from Vertica using sqlalchemy.
    This is not efficient for large data, it should be rewritten using verticapy
    '''

    def __init__(
        self,
        table: str,
        host: str,
        user: str,
        password: str,
        database: str,
        schema: str,
        port: int = 5433
    ):

        # TODO: use kwargs here
        self.connection_url = f'vertica+vertica_python://{user}:{password}@{host}:{port}/{database}'
        super().__init__(table, host, port, user, password, database, schema)
    
    def to_dask(self) -> DaskDataFrame:
        raise NotImplementedError
    
    def push_dask(self, data: DaskDataFrame):
        raise NotImplementedError
    
    def _check_validity(self) -> bool:
        raise NotImplementedError

