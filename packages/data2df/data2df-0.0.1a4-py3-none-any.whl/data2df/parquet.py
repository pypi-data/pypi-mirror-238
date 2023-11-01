from pathlib import Path

from .base import BaseDevice
from .manage_requirements import require_package, PandasDataFrame, DaskDataFrame, PySparkDataFrame, PolarsDataFrame


class Parquet(BaseDevice):
    def __init__(
        self,
        path: str,
        push_pandas_kwargs: dict = {},
        to_pandas_kwargs: dict = {},
        push_dask_kwargs: dict = {},
        to_dask_kwargs: dict = {},
        push_pyspark_kwargs: dict = {},
        to_pyspark_kwargs: dict = {},
        push_polars_kwargs: dict = {},
        to_polars_kwargs: dict = {},
    ):
        '''
        :param path: Location of the CSV file or file-like object
        '''
        self.path = Path(path)
        super().__init__(
            push_pandas_kwargs=push_pandas_kwargs,
            to_pandas_kwargs=to_pandas_kwargs,
            push_dask_kwargs=push_dask_kwargs,
            to_dask_kwargs=to_dask_kwargs,
            push_pyspark_kwargs=push_pyspark_kwargs,
            to_pyspark_kwargs=to_pyspark_kwargs,
            push_polars_kwargs=push_polars_kwargs,
            to_polars_kwargs=to_polars_kwargs,
        )

    @require_package('pandas')
    def push_pandas(self, data: PandasDataFrame) -> None:
        if self.path.is_dir():
            raise NotImplementedError('Pandas does not support partitioned parquets')

        data.to_parquet(self.path, **(self.push_pandas_kwargs))

    @require_package('pandas')
    def to_pandas(self) -> PandasDataFrame:
        if self.path.is_dir():
            raise NotImplementedError('Pandas does not support partitioned parquets')

        data = pandas.read_parquet(self.path, **(self.to_pandas_kwargs))  # noqa: F821
        return data

    @require_package('dask')
    def push_dask(self, data: DaskDataFrame):
        # Dask does not support writing to a single file
        # This is a hack, not sure if I should drop the support for this
        # Maybe if I create a common method for Dask and Spark it will look nice
        if self.path.is_file():
            if self.push_dask_kwargs['append']:
                raise NotImplementedError('Appending to single parquet files is not supported from Dask')
            if self.push_dask_kwargs['overwrite']:
                # Logic: force Dask to write only one parquet in a temp dir
                # Then move and rename the parquet file and rm the temp dir
                self.path.unlink()
                data.repartition(1)\
                    .to_parquet(self.path.parents[0]/'tmp_parquet', **(self.push_dask_kwargs))

                (self.path.parents[0]/'tmp_parquet'/'part.0.parquet').rename(self.path)
                (self.path.parents[0]/'tmp_parquet').rmdir()

                return None

            raise FileExistsError(f'{self.path} already exists.')
            #raise NotImplementedError('Dask does not support writing single-file parquets')

        data.to_parquet(self.path, **(self.push_dask_kwargs))

    @require_package('dask')
    def to_dask(self) -> DaskDataFrame:
        data = dask.dataframe.read_parquet(self.path, **(self.to_dask_kwargs))  # noqa: F821
        return data

    @require_package('pyspark')
    def to_pyspark(self) -> PySparkDataFrame:
        raise NotImplementedError

    @require_package('pyspark')
    def push_pyspark(self, data: PySparkDataFrame):
        raise NotImplementedError

    @require_package('polars')
    def to_polars(self) -> PolarsDataFrame:
        raise NotImplementedError

    @require_package('polars')
    def push_polars(self, data: PolarsDataFrame):
        raise NotImplementedError

    def _check_validity(self) -> bool:
        raise NotImplementedError
