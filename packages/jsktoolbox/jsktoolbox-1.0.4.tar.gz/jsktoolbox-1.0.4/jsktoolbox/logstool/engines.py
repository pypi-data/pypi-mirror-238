# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose: logger engine classes.
"""

import os
import sys
from abc import ABC, abstractmethod
from inspect import currentframe

from typing import Optional, List, Dict
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import Env, PathChecker

# https://www.geeksforgeeks.org/python-testing-output-to-stdout/


class ILoggerEngine(ABC):
    """Logger engine interface class."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send message method."""


class LoggerEngineStdout(ILoggerEngine, BData, NoDynamicAttributes):
    """STDOUT Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to STDOUT."""
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self.data["buffered"]:
            sys.stdout.flush()


class LoggerEngineStderr(ILoggerEngine, BData, NoDynamicAttributes):
    """STDERR Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to STDERR."""
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self.data["buffered"]:
            sys.stderr.flush()


class LoggerEngineFile(ILoggerEngine, BData, NoDynamicAttributes):
    """FILE Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to file."""

    @property
    def logdir(self) -> Optional[str]:
        """Return log directory."""
        if "dir" not in self.data:
            self.data["dir"] = None
        return self.data["dir"]

    @logdir.setter
    def logdir(self, dirname: str) -> None:
        """Set log directory."""
        if dirname[-1] != os.sep:
            dirname = f"{dirname}/"
        ld = PathChecker(dirname)
        if not ld.exists:
            ld.create()
        if ld.exists and ld.is_dir:
            self.data["dir"] = ld.path

    @property
    def logfile(self) -> Optional[str]:
        """Return log file name."""
        if "file" not in self.data:
            self.data["file"] = None
        return self.data["file"]

    @logfile.setter
    def logfile(self, filename: str) -> None:
        """Set log file name."""
        # TODO: check procedure
        fn = None
        if self.logdir is None:
            fn = filename
        else:
            fn = os.path.join(self.logdir, filename)
        ld = PathChecker(fn)
        if ld.exists:
            if not ld.is_file:
                raise Raise.error(
                    f"The filename passed: '{filename}' is a directory.",
                    FileExistsError,
                    self.__class__.__name__,
                    currentframe(),
                )
        else:
            if not ld.create():
                raise Raise.error(
                    f"I cannot create a file: {ld.path}",
                    PermissionError,
                    self.__class__.__name__,
                    currentframe(),
                )
        self.logdir = ld.dirname
        self.data["file"] = ld.filename


class LoggerEngineSyslog(ILoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(self, buffered: bool = False) -> None:
        """Constructor."""
        self.data["buffered"] = buffered

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""


# #[EOF]#######################################################################
