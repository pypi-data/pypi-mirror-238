import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .factor import factor
from .match import match
from .map_to_index import map_to_index
from .intersect import intersect
from .union import union
from .subset import subset
from .is_list_of_type import is_list_of_type
from .normalize_subscript import normalize_subscript
from .print_truncated import print_truncated, print_truncated_list, print_truncated_dict
from .print_wrapped_table import print_wrapped_table, create_floating_names, truncate_strings, print_type
