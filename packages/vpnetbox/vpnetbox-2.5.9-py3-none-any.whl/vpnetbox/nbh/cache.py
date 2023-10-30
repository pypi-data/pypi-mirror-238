"""Cache, read/write NbData from/to pickle file."""

from __future__ import annotations

import logging
import os
import pickle
import re
from pathlib import Path
from typing import Any

from vpnetbox.types_ import DAny


class Cache:
    """Cache, read/write NbData from/to pickle file."""

    def __init__(self, nbd, cache_path: str = "", **kwargs):
        """Init Cache.

        :param nbd: NbData object to be cached.
        :param cache_path: Path to the pickle file.
        """
        _ = kwargs
        self.nbd = nbd
        self.path: Path = _init_path(cache_path)

    def __repr__(self) -> str:
        """__repr__."""
        name = self.__class__.__name__
        return f"<{name}: {self.path.name}>"

    # =========================== method =============================

    def is_cache(self) -> bool:
        """Check if a pickle file is present on disk.

        :return: True if the pickle file is present, False otherwise.
        """
        return self.path.is_file()

    def read_cache(self) -> None:
        """Read cached data from a pickle file.

        :return: None. Update self object.
        """
        self._read_cache()
        self._logging_debug__loaded()

    def write_cache(self) -> None:
        """Write cache to a pickle file.

        :return: None. Update a pickle file.
        """
        attrs = [
            *list(getattr(self.nbd, "_helper_attrs")),
            *list(getattr(self.nbd, "_data_attrs")),
        ]
        data = {s: getattr(self.nbd, s) for s in attrs}

        try:
            self._create_dir()
            self._create_file(data)
        except PermissionError as ex:
            self._error__cmd_chmod(ex)
            raise type(ex)(*ex.args)

        self._logging_debug__saved()

    # ====================== helpers ======================

    def _create_dir(self) -> None:
        """Create directory for cache."""
        if not self.path:
            return
        path = Path(self.path)
        root = path.resolve().parent
        if not root.is_dir():
            root.mkdir(parents=True, exist_ok=True)

    def _create_file(self, data: DAny) -> None:
        """Create pickl file for cache with write permissions 666.

        :param data: Data that need be saved to pickle file.
        :return: None. Update pickle file.
        """
        os.umask(0)
        descriptor = os.open(
            path=str(self.path),
            flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
            mode=0o666
        )
        with open(descriptor, "wb") as fh:
            pickle.dump(data, fh)

    def _read_cache(self) -> None:
        """Read cached data from a pickle file.

        :return: None. Update
        """
        try:
            with self.path.open(mode="rb") as fh:
                data: DAny = dict(pickle.load(fh))
                for attr, value in data.items():
                    setattr(self.nbd, attr, value)
        except FileNotFoundError as ex:
            if hasattr(ex, "args") and isinstance(ex.args, tuple):
                msgs = [s for s in ex.args if isinstance(s, str)]
                for attr in ["filename", "filename2"]:
                    if hasattr(ex, attr) and getattr(ex, attr):
                        msgs.append(f"{ex.filename}")
                msg = "To create *.pickle file need to execute vpnetbox without --cache parameter."
                msgs.append(msg)
                msg = ". ".join(msgs)
                raise FileNotFoundError(msg) from ex
            raise FileNotFoundError(*ex.args) from ex

    # =========================== logging ============================

    def _error__cmd_chmod(self, ex: Any) -> None:
        """Log ERROR, with example how to solve problem: chmod {path}."""
        error = f"{type(ex).__name__}: {ex}"
        path = (re.findall(r"(\'.+\')$", str(ex)) or [str(self.path)])[0]
        cmd = f"\"sudo chmod o+rw {path}\""
        msg = f"{error}. Please change permissions by command: {cmd} and try again."
        logging.error(msg)

    def _logging_debug__loaded(self) -> None:
        """Log DEBUG cache loaded."""
        path = str(self.path)
        msg = f"cache loaded from {path=}"
        logging.debug(msg)

    def _logging_debug__saved(self) -> None:
        """Log DEBUG cache saved."""
        path = str(self.path)
        msg = f"cache saved to {path=}"
        logging.debug(msg)


# ============================= helpers ==============================

def _init_path(cache_path: str) -> Path:
    """Init path to cache pickle file."""
    if cache_path:
        return Path(cache_path)
    return Path("Cache.pickle")
