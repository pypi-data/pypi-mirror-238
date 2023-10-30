# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 05.09.2023

  Purpose: various classes of interaction with the system.
"""

import os
from inspect import currentframe
from pathlib import Path
from typing import Optional, List

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData


class Env(NoDynamicAttributes):
    """Environment class."""

    @classmethod
    @property
    def home(cls) -> str:
        """Return home dir name."""
        return os.getenv("HOME")

    @classmethod
    @property
    def username(cls) -> str:
        """Return login name."""
        return os.getenv("USER")


class PathChecker(BData, NoDynamicAttributes):
    """PathChecker class for filesystem path."""

    def __init__(self, pathname: str, check_deep: bool = True) -> None:
        """Constructor."""
        if pathname is None:
            raise Raise.error(
                "pathname as string expected, not None.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if not isinstance(pathname, str):
            raise Raise.error(
                f"pathname as string expected, '{type(pathname)}' received.",
                TypeError,
                self.__class__.__name__,
                currentframe(),
            )
        if isinstance(pathname, str) and len(pathname) == 0:
            raise Raise.error(
                "pathname cannot be an empty string.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        self.data["pathname"] = pathname
        self.data["split"] = check_deep
        self.data["list"]: List = []
        # analysis
        self.__run__()

    def __run__(self) -> None:
        """Path analysis procedure."""
        query = Path(self.data["pathname"])
        # check exists
        self.data["exists"] = query.exists()
        if self.data["exists"]:
            # check isfile
            self.data["isfile"] = query.is_file()
            # check isdir
            self.data["isdir"] = query.is_dir()
            # check issymlink
            self.data["issymlink"] = query.is_symlink()
            # resolve symlink
            self.data["posixpath"] = str(query.resolve())

        if self.data["split"]:
            # split and analyse
            tmp = ""
            for item in self.path.split(os.sep):
                if item == "":
                    continue
                tmp += f"{os.sep}{item}"
                self.data["list"].append(PathChecker(tmp, False))

    def __str__(self) -> str:
        """Return class data as string."""
        return (
            "PathChecker("
            f"'pathname': '{self.path}', "
            f"'exists': '{self.exists}', "
            f"'is_dir': '{self.is_dir if self.exists else ''}', "
            f"'is_file': '{self.is_file if self.exists else ''}', "
            f"'is_symlink': '{self.is_symlink if self.exists else ''}', "
            f"'posixpath': '{self.posixpath if self.exists else ''}'"
            ")"
        )

    def __repr__(self) -> str:
        """Return string representation."""
        return f"PathChecker('{self.path}')"

    @property
    def dirname(self) -> Optional[str]:
        """Return dirname from path."""
        if self.exists:
            last = None
            for item in self.data["list"]:
                if item.is_dir:
                    last = item.path
            return last
        return None

    @property
    def filename(self) -> Optional[str]:
        """Return filename from path."""
        if self.exists and self.is_file:
            tmp = self.path.split(os.sep)
            if len(tmp) > 0:
                if tmp[-1] != "":
                    return tmp[-1]
        return None

    @property
    def exists(self) -> bool:
        """Return path exists flag."""
        if "exists" in self.data:
            return self.data["exists"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_dir(self) -> bool:
        """Return path isdir flag."""
        if "isdir" in self.data:
            return self.data["isdir"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_file(self) -> bool:
        """Return path isfile flag."""
        if "isfile" in self.data:
            return self.data["isfile"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def is_symlink(self) -> bool:
        """Return path issymlink flag."""
        if "issymlink" in self.data:
            return self.data["issymlink"]
        else:
            raise Raise.error(
                "Unexpected exception",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    @property
    def path(self) -> str:
        """Return path string."""
        return self.data["pathname"]

    @property
    def posixpath(self) -> Optional[str]:
        """Return path string."""
        if self.exists:
            return self.data["posixpath"]
        return None

    def create(self) -> bool:
        """Create path procedure."""
        test_path = self.path
        file = True
        if self.path[-1] == os.sep:
            file = False
            test_path = self.path[:-1]
        for item in self.data["list"]:
            if item.exists:
                continue
            if item.path == test_path:
                # last element
                if file:
                    # touch file
                    with open(item.path, "w") as fp:
                        pass
                else:
                    os.mkdir(item.path)
            else:
                os.mkdir(item.path)
        # check
        self.data["list"] = []
        self.__run__()

        return self.exists


# #[EOF]#######################################################################
