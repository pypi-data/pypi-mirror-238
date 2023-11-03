# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: Main class for creating and processes config files.
"""

import re
from inspect import currentframe
from typing import List, Dict, Optional, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.configtool.libs.file import FileProcessor
from jsktoolbox.configtool.libs.data import DataProcessor


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def VARNAME(self) -> str:
        """Return FP key."""
        return "__varname__"

    @classmethod
    @property
    def VALUE(self) -> str:
        """Return FP key."""
        return "__value__"

    @classmethod
    @property
    def DESC(self) -> str:
        """Return FP key."""
        return "__desc__"

    @classmethod
    @property
    def FP(self) -> str:
        """Return FP key."""
        return "__file_processor__"

    @classmethod
    @property
    def DP(self) -> str:
        """Return DP key."""
        return "__data_processor__"

    @classmethod
    @property
    def RE_SECTION(self) -> str:
        """Return RE_SECTION key."""
        return "__re_section__"

    @classmethod
    @property
    def RE_VAR(self) -> str:
        """Return RE_VAR key."""
        return "__re_variable__"

    @classmethod
    @property
    def RE_DESC(self) -> str:
        """Return RE_DESC key."""
        return "__re_description__"

    @classmethod
    @property
    def RE_INT(self) -> str:
        """Return RE_INT key."""
        return "__re_integer__"

    @classmethod
    @property
    def RE_FLOAT(self) -> str:
        """Return RE_FLOAT key."""
        return "__re_float__"

    @classmethod
    @property
    def RE_BOOL(self) -> str:
        """Return RE_BOOL key."""
        return "__re_bool__"

    @classmethod
    @property
    def RE_TRUE(self) -> str:
        """Return RE_TRUE key."""
        return "__re_true__"

    @classmethod
    @property
    def RE_FALSE(self) -> str:
        """Return RE_FALSE key."""
        return "__re_false__"

    @classmethod
    @property
    def RE_LIST(self) -> str:
        """Return RE_LIST key."""
        return "__re_list__"


class Config(BData, NoDynamicAttributes):
    """Config main class."""

    def __init__(
        self,
        filename: str,
        main_section_name: str,
        auto_create: bool = False,
    ) -> None:
        """Constructor."""
        self._data[Keys.FP] = FileProcessor()
        self._data[Keys.DP] = DataProcessor()
        self.__fp.file = filename
        self.__dp.main_section = main_section_name
        if auto_create:
            if not self.__fp.file_exists:
                self.__fp.file_create()
        # compile regex
        self._data[Keys.RE_SECTION] = re.compile(r"\s{0,}\[.*\]\s{0,}")
        self._data[Keys.RE_DESC] = re.compile(r"\s{0,}#")
        self._data[Keys.RE_VAR] = re.compile(r"\s{0,}\S{1,}\s{0,}=")
        self._data[Keys.RE_INT] = re.compile(r"^\d{1,}$")
        self._data[Keys.RE_FLOAT] = re.compile(r"^\d{1,}\.\d{1,}$")
        self._data[Keys.RE_BOOL] = re.compile(
            r"^true|false|yes|no$", re.IGNORECASE
        )
        self._data[Keys.RE_TRUE] = re.compile(r"^true|yes$", re.IGNORECASE)
        self._data[Keys.RE_FALSE] = re.compile(r"^false|no$", re.IGNORECASE)
        self._data[Keys.RE_LIST] = re.compile(r"^\[.*\]$")

    @property
    def __fp(self) -> FileProcessor:
        """Return FileProcessor object."""
        return self._data[Keys.FP]

    @property
    def __dp(self) -> DataProcessor:
        """Return DataProcessor object."""
        return self._data[Keys.DP]

    @property
    def file_exists(self) -> bool:
        """Check if file exists."""
        return self.__fp.file_exists

    def __value_parser(self, item: str) -> Any:
        """Return proper type of value."""
        if self._data[Keys.RE_BOOL].match(item):
            return True if self._data[Keys.RE_TRUE].match(item) else False
        elif self._data[Keys.RE_INT].match(item):
            return int(item)
        elif self._data[Keys.RE_FLOAT].match(item):
            return float(item)
        elif self._data[Keys.RE_LIST].match(item):
            out = []
            tmp = [x.strip() for x in item.strip("[]").split(",")]
            for item in tmp:
                out.append(self.__value_parser(item))
            return out
        return str(item.strip("\"'"))

    def __var_parser(self, line: str) -> Dict:
        """Return Dict[varname, value, desc]."""
        out = {
            Keys.VARNAME: None,
            Keys.VALUE: None,
            Keys.DESC: None,
        }
        tmp = line.split("=", 1)
        if len(tmp) != 2:
            raise Raise.error(
                f"Unexpected config line format: '{line}'",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )
        out[Keys.VARNAME] = tmp[0].strip()
        if len(tmp[1]) > 0:
            tmp = tmp[1].split("#", 1)
            # desc
            if len(tmp) == 2 and len(tmp[1]) > 0:
                out[Keys.DESC] = tmp[1].strip()
            # value
            out[Keys.VALUE] = self.__value_parser(tmp[0].strip())

        return out

    def load(self) -> bool:
        """Load config file to DataProcessor."""
        test = False
        # 1. load file into list
        file: List[str] = self.__fp.readlines()
        section_name: str = self.__dp.main_section
        for line in file:
            # check section
            if self._data[Keys.RE_SECTION].match(line):
                section_name = self.__dp.add_section(line)
            # check description
            elif self._data[Keys.RE_DESC].match(line):
                self.__dp.set(section_name, desc=line.strip("# "))
            # check var
            elif self._data[Keys.RE_VAR].match(line):
                out = self.__var_parser(line)
                self.__dp.set(
                    section=section_name,
                    varname=out[Keys.VARNAME],
                    value=out[Keys.VALUE],
                    desc=out[Keys.DESC],
                )
            else:
                self.__dp.set(section_name, desc=line)
            test = True
        return test

    def save(self) -> bool:
        """Save config file from DataProcessor."""
        test = False
        self.__fp.write(self.__dp.dump)
        test = True
        return test

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Any:
        """Get and return data."""
        return self.__dp.get(section, varname, desc)

    def set(
        self,
        section: str,
        varname: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Set data."""
        self.__dp.set(section, varname, value, desc)


# #[EOF]#######################################################################
