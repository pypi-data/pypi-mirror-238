import hashlib
import os
import sys
from functools import partial
from typing import Optional

import attrs
from dvc_data.hashfile.db.local import LocalHashFileDB
from dvc_objects.fs.callbacks import Callback
from dvc_objects.fs.local import LocalFileSystem

if sys.version_info < (3, 9):
    sha256 = hashlib.sha256
else:
    sha256 = partial(hashlib.sha256, usedforsecurity=False)


@attrs.frozen
class UniqueId:
    storage: str
    parent: str
    name: str
    etag: str
    size: int
    vtype: str
    location: Optional[str]

    @property
    def path(self) -> str:
        return f"{self.parent}/{self.name}" if self.parent else self.name

    def get_hash(self) -> str:
        etag = f"{self.vtype}{self.location}" if self.vtype else self.etag
        return sha256(
            f"{self.storage}/{self.parent}/{self.name}/{etag}".encode()
        ).hexdigest()


class DQLCache:
    def __init__(self, cache_dir: str, tmp_dir: str):
        self.odb = LocalHashFileDB(
            LocalFileSystem(),
            cache_dir,
            tmp_dir=tmp_dir,
        )

    def get_path(self, uid: UniqueId) -> Optional[str]:
        if self.contains(uid):
            return self.path_from_checksum(uid.get_hash())
        return None

    def contains(self, uid: UniqueId) -> bool:
        return self.odb.exists(uid.get_hash())

    def path_from_checksum(self, checksum: str) -> str:
        assert checksum
        return self.odb.oid_to_path(checksum)

    def download(self, uid: UniqueId, fs, callback=None) -> None:
        from_path = f"{uid.storage}/{uid.path}"
        from dvc_objects.fs.utils import tmp_fname

        path = self.odb.fs.path
        tmp_info = path.join(self.odb.tmp_dir, tmp_fname())  # type: ignore[arg-type]
        size = uid.size
        if size < 0:
            size = fs.size(from_path)
        with Callback.as_tqdm_callback(
            callback,
            desc=path.name(from_path),
            bytes=True,
            size=size,
        ) as cb:
            fs.get_file(from_path, tmp_info, callback=cb)

        try:
            oid = uid.get_hash()
            self.odb.add(tmp_info, self.odb.fs, oid)
        finally:
            os.unlink(tmp_info)

    def store_data(self, uid: UniqueId, contents: bytes, callback=None) -> None:
        checksum = uid.get_hash()
        dst = self.path_from_checksum(checksum)
        if not os.path.exists(dst):
            # Create the file only if it's not already in cache
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, mode="wb") as f:
                f.write(contents)
        if callback:
            callback.relative_update(len(contents))

    def clear(self):
        """
        Completely clear the cache.
        """
        self.odb.clear()
