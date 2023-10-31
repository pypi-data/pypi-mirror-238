import importlib
from functools import wraps


def require_package(package_name):
    """Imports a package. Raise an exception if package is not present
    @require_package('pyspark')
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                package = importlib.import_module(package_name)
                if package_name == 'dask':
                    import pdb
                    pdb.set_trace
                func.__globals__[package_name] = package
                return func(*args, **kwargs)
            except ImportError as e:
                raise ImportError(
                    f"{package_name} is not installed. Please install {package_name} to use this functionality."
                ) from e

        return wrapper

    return decorator
