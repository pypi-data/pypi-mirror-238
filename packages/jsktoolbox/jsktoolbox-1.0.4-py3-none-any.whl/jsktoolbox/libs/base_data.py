# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 01.09.2023

  Purpose: BData container base class.
"""
import inspect
from typing import Dict, Optional
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise


class BData(NoDynamicAttributes):
    """BData container class."""

    __data: Optional[Dict] = None

    @property
    def _data(self) -> Dict:
        """Return data dict."""
        if self.__data is None:
            self.__data = {}
        return self.__data

    @_data.setter
    def _data(self, value: Optional[Dict]) -> None:
        """Set data dict."""
        if value is None:
            self.__data = {}
            return
        if isinstance(value, Dict):
            for key in value.keys():
                self.__data[key] = value[key]
        else:
            raise Raise.error(
                f"Dict type expected, '{type(value)}' received.",
                AttributeError,
                self.__class__.__name__,
                inspect.currentframe,
            )


# #[EOF]#######################################################################
