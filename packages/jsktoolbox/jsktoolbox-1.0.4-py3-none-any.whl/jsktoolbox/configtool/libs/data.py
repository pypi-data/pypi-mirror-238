# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: DataProcessor class for processing dataset operations.
"""

from inspect import currentframe
from typing import List, Tuple, Optional, Union, Any, TypeVar
from abc import ABC, abstractmethod
from copy import copy
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData

TVariableModel = TypeVar("TVariableModel", bound="VariableModel")


class Keys(NoDynamicAttributes):
    """Keys definition class.

    For internal purpose only.
    """

    @classmethod
    @property
    def DATA(self) -> str:
        """Return data key."""
        return "__data__"

    @classmethod
    @property
    def DESC(self) -> str:
        """Return desc key."""
        return "__desc__"

    @classmethod
    @property
    def DESCRIPTION(self) -> str:
        """Return description key."""
        return "__description__"

    @classmethod
    @property
    def MAIN(self) -> str:
        """Return main key."""
        return "__main__"

    @classmethod
    @property
    def NAME(self) -> str:
        """Return name key."""
        return "__name__"

    @classmethod
    @property
    def VALUE(self) -> str:
        """Return value key."""
        return "__value__"

    @classmethod
    @property
    def VARIABLES(self) -> str:
        """Return variables key."""
        return "__variables__"


class IModel(ABC):
    """Model class interface."""

    @property
    @abstractmethod
    def dump(self) -> Union[List[str], TVariableModel]:
        """Dump data."""

    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        """Get name property."""

    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        """Set name property."""

    @abstractmethod
    def parser(self, value: str) -> None:
        """Parser method."""

    @abstractmethod
    def search(self, name: str) -> bool:
        """Search method."""


class VariableModel(BData, IModel, NoDynamicAttributes):
    """VariableModel class."""

    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[Union[str, int, float, bool, List]] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Constructor."""
        self._data[Keys.NAME] = name
        self._data[Keys.VALUE] = value
        self._data[Keys.DESC] = desc

    def __repr__(self) -> str:
        """Return representation class string."""
        tmp = ""
        tmp += f"name='{self.name}', " if self.name is not None else ""
        if isinstance(self.value, (int, float, bool)):
            tmp += f"value={self.value}, " if self.value is not None else ""
        elif isinstance(self.value, List):
            tmp += (
                f"value=[{self.value}], " if self.value is not None else ""
            )
        else:
            tmp += (
                f"value='{self.value}', " if self.value is not None else ""
            )
        tmp += f"desc='{self.desc}'" if self.desc is not None else ""
        return f"{self.__class__.__name__}({tmp})"

    def __str__(self) -> str:
        """Return formated string."""
        tmp = ""
        tmp += f"{self.name} = " if self.name is not None else ""
        if isinstance(self.value, (int, float, bool)):
            tmp += f"{self.value}" if self.value is not None else ""
        elif isinstance(self.value, List):
            tmp += f"{self.value}" if self.value is not None else ""
        else:
            tmp += (
                '"{}"'.format(self.value.strip("\"'"))
                if self.value is not None
                else ""
            )
        if tmp:
            tmp += f" # {self.desc}" if self.desc is not None else ""
        else:
            tmp += f"# {self.desc}" if self.desc is not None else "#"
        return tmp

    @property
    def desc(self) -> Optional[str]:
        """Get descrption property."""
        return self._data[Keys.DESC]

    @desc.setter
    def desc(self, desc: Optional[str]) -> None:
        """Set description property."""
        self._data[Keys.DESC] = desc

    @property
    def dump(self) -> TVariableModel:
        """Dump data."""
        return self

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data[Keys.NAME]

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Set name property."""
        self._data[Keys.NAME] = name.strip()

    def parser(self, value: str) -> None:
        """Parser method."""

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def value(self) -> Optional[Union[str, int, float, bool, List]]:
        """Get value property."""
        return self._data[Keys.VALUE]

    @value.setter
    def value(
        self, value: Optional[Union[str, int, float, bool, List]]
    ) -> None:
        """Set value property."""
        self._data[Keys.VALUE] = value


class SectionModel(BData, IModel, NoDynamicAttributes):
    """SectionModel class."""

    def __init__(self, name: Optional[str] = None) -> None:
        """Constructor."""
        self._data[Keys.NAME] = None
        self._data[Keys.VARIABLES]: List[VariableModel] = []
        self.parser(name)

    def __repr__(self) -> str:
        """Return representation class string."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Return formated string."""
        return f"[{self.name}]"

    @property
    def dump(self) -> List[Any]:
        """Dump data."""
        tmp = []
        tmp.append(self)
        for item in self._data[Keys.VARIABLES]:
            tmp.append(item.dump())
        return copy(tmp)

    def parser(self, value: str) -> None:
        """Parser method."""
        if value is None:
            return
        tmp = f"{value}".strip("[] \n")
        if tmp:
            self._data[Keys.NAME] = tmp
        else:
            raise Raise.error(
                f"String name expected, '{tmp}' received.",
                ValueError,
                self.__class__.__name__,
                currentframe(),
            )

    def search(self, name: str) -> bool:
        """Search method."""
        return self.name == name

    @property
    def name(self) -> Optional[str]:
        """Get name property."""
        return self._data[Keys.NAME]

    @name.setter
    def name(self, name: str) -> None:
        """Set name property."""
        self.parser(name)

    def get_variable(self, name: str) -> Optional[VariableModel]:
        """Search and return VariableModel if exists."""
        name = str(name)
        for item in self._data[Keys.VARIABLES]:
            if item.name == name:
                return item
        return None

    def set_variable(
        self,
        name: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Add or update VariableModel."""
        if name is not None:
            item: VariableModel = self.get_variable(name)
            if item is not None:
                if value is not None or (value is None and desc is None):
                    item.value = value
                if desc is not None or (desc is None and value is None):
                    item.desc = desc
                return
        # add new VariableModel
        if name is None and value is not None:
            return
        self._data[Keys.VARIABLES].append(VariableModel(name, value, desc))

    @property
    def variables(self) -> List[VariableModel]:
        """Return list of VariableModel."""
        return self._data[Keys.VARIABLES]


class DataProcessor(BData, NoDynamicAttributes):
    """DataProcessor class."""

    def __init__(self) -> None:
        """Constructor."""
        self._data[Keys.DATA] = []

    @property
    def main_section(self) -> Optional[str]:
        """Return main section name."""
        if Keys.MAIN not in self._data:
            self._data[Keys.MAIN] = None
        return self._data[Keys.MAIN]

    @main_section.setter
    def main_section(self, name: str) -> None:
        """Set main section name."""
        if not isinstance(name, str):
            name = str(name)
        self._data[Keys.MAIN] = name
        self.add_section(name)

    @property
    def sections(self) -> Tuple:
        """Return sections keys tuple."""
        out = []
        for item in self._data[Keys.DATA]:
            out.append(item.name)
        return tuple(sorted(out))

    def add_section(self, name: str) -> str:
        """Add section object to dataset.

        Return: extracted section name.
        """
        sm = SectionModel(str(name))
        if sm.name not in self.sections:
            self._data[Keys.DATA].append(sm)
        return sm.name

    def get_section(self, name: str) -> Optional[SectionModel]:
        """Get section object if exists."""
        sm = SectionModel(name)
        for item in self._data[Keys.DATA]:
            if item.name == sm.name:
                return item
        return None

    def set(
        self,
        section: str,
        varname: Optional[str] = None,
        value: Optional[Any] = None,
        desc: Optional[str] = None,
    ) -> None:
        """Set data to [SectionModel]->[VariableModel]."""
        section_name = self.add_section(section)
        found_section = self.get_section(section_name)
        found_section.set_variable(varname, value, desc)

    def get(
        self, section: str, varname: Optional[str] = None, desc: bool = False
    ) -> Optional[Any]:
        """Return value."""
        sm = SectionModel(section)
        if sm.name in self.sections:
            found_section = self.get_section(section)
            if varname is not None:
                found_var = found_section.get_variable(varname)
                if found_var is not None:
                    if desc:
                        # Return description for varname
                        return found_var.desc
                    else:
                        # Return value for varname
                        return found_var.value
                else:
                    return None
            else:
                # Return list od description for section
                out = []
                for item in found_section.variables:
                    if item.name is None and item.desc is not None:
                        out.append(item.desc)
                return out
        else:
            raise Raise.error(
                f"Given section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )

    def __dump(self, section: str) -> str:
        """Return formatted configuration data for section name."""
        out = ""
        if section in self.sections:
            found_section = self.get_section(section)
            out += f"{found_section}\n"
            for item in found_section.variables:
                out += f"{item}\n"
            out += (
                f"# :::::<End of section: '{found_section.name}'>:::::\n\n"
            )
        else:
            raise Raise.error(
                f"Section name: '{section}' not found.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )
        return out

    @property
    def dump(self) -> str:
        """Return formated configuration data string."""
        out = ""

        # first section is a main section
        if self.main_section is None:
            raise Raise.error(
                "Main section is not set.",
                KeyError,
                self.__class__.__name__,
                currentframe(),
            )
        out = self.__dump(self.main_section)

        # other sections
        for section in tuple(set(self.sections) ^ set([self.main_section])):
            out += self.__dump(section)

        return out


# #[EOF]#######################################################################
