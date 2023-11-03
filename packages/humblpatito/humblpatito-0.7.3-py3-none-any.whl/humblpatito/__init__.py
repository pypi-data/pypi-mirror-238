"""humblpatito, a data-modelling library built on top of polars and pydantic."""
from polars import Expr, Series, col

from humblpatito import exceptions, sql
from humblpatito.exceptions import DataFrameValidationError
from humblpatito.polars import DataFrame, LazyFrame
from humblpatito.pydantic import Field, Model

_CACHING_AVAILABLE = False
_DUCKDB_AVAILABLE = False
field = col("_")
__all__ = [
    "DataFrame",
    "DataFrameValidationError",
    "Expr",
    "Field",
    "LazyFrame",
    "Model",
    "Series",
    "_CACHING_AVAILABLE",
    "_DUCKDB_AVAILABLE",
    "col",
    "exceptions",
    "field",
    "sql",
]

try:
    from humblpatito import duckdb

    _DUCKDB_AVAILABLE = True
    __all__ += ["duckdb"]
except ImportError:  # pragma: no cover
    pass

try:
    from humblpatito.database import Database

    _CACHING_AVAILABLE = True
    __all__ += ["Database"]
except ImportError:
    pass


try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
