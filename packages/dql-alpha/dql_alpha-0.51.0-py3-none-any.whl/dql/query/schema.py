import json
from datetime import datetime, timezone
from random import getrandbits
from typing import Any, Callable, Dict, Optional, Tuple

from sqlalchemy.sql.elements import ColumnClause
from sqlalchemy.sql.visitors import TraversibleType

from dql.data_storage.abstract import RANDOM_BITS
from dql.sql.types import JSON, Boolean, DateTime, Int, String


class ColumnMeta(TraversibleType):
    def __getattr__(cls, name: str):  # noqa: B902
        return cls(name)  # pylint: disable=no-value-for-parameter


class Object:
    """
    Object is used as a placeholder parameter to indicate the actual stored object
    being passed as a parameter to the UDF.
    """

    def __init__(self, reader: Callable, cache: bool = False):
        """
        Initialize the object and specify the reader to be
        used for loading the object into memory.
        """
        self.reader = reader
        self.cache = cache


class LocalFilename:
    """
    Placeholder parameter representing the local path to a cached copy of the object.
    """

    def __init__(self, glob: str = None):
        """
        Initialize the object and specify the file mask to be returned.
        If glob is None, then all files will be returned. If glob is specified,
        then only files matching the glob will be returned,
        otherwise None will be returned.
        """
        self.glob = glob


class Column(ColumnClause, metaclass=ColumnMeta):  # pylint: disable=abstract-method
    inherit_cache: Optional[bool] = True

    def __init__(self, text, type_=None, is_literal=False, _selectable=None):
        self.name = text
        super().__init__(
            text, type_=type_, is_literal=is_literal, _selectable=_selectable
        )

    def glob(self, glob_str):
        return self.op("GLOB")(glob_str)


class DatasetRow:
    schema = (
        ("source", String),
        ("parent", String),
        ("name", String),
        ("size", Int),
        ("location", JSON),
        ("vtype", String),
        ("dir_type", Int),
        ("owner_name", String),
        ("owner_id", String),
        ("is_latest", Boolean),
        ("last_modified", DateTime),
        ("version", String),
        ("etag", String),
        ("checksum", String),
        ("anno", JSON),
        # system column
        ("random", Int),
    )

    @staticmethod
    def create(
        name: str,
        source: str = "",
        parent: str = "",
        size: int = 0,
        location: Dict[str, Any] = None,
        vtype: str = "",
        dir_type: int = 0,
        owner_name: str = "",
        owner_id: str = "",
        is_latest: bool = True,
        last_modified: datetime = None,
        version: str = "",
        etag: str = "",
        checksum: str = "",
        anno: Dict[str, Any] = None,
    ) -> Tuple[
        str,
        str,
        str,
        int,
        Optional[str],
        str,
        int,
        str,
        str,
        bool,
        datetime,
        str,
        str,
        str,
        Optional[str],
        int,
    ]:
        if location:
            location = json.dumps([location])  # type: ignore [assignment]

        if anno:
            anno = json.dumps(anno)  # type: ignore [assignment]

        last_modified = last_modified or datetime.now(timezone.utc)

        random = getrandbits(RANDOM_BITS)

        return (  # type: ignore [return-value]
            source,
            parent,
            name,
            size,
            location,
            vtype,
            dir_type,
            owner_name,
            owner_id,
            is_latest,
            last_modified,
            version,
            etag,
            checksum,
            anno,
            random,
        )


C = Column
