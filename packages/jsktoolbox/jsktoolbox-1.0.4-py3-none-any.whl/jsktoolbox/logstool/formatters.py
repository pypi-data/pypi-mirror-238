# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose:
"""

import os
import sys
from abc import ABC, abstractmethod
from inspect import currentframe

from typing import Optional, List, Dict, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

#  https://www.programiz.com/python-programming/datetime/strftime


class BLogFormatter(NoDynamicAttributes):
    """Log formatter base class."""

    __template: Optional[str] = None
    __forms: Optional[List] = None

    def __init__(self) -> None:
        """Constructor."""
        self.__template = "{}"
        self.__forms = []

    def format(self, messages: str) -> str:
        """Method for format message string."""

    @property
    def _forms_(self) -> List:
        """Get forms list."""
        return self.__forms

    @_forms_.setter
    def _forms_(self, item: Any) -> None:
        """Set forms list."""
        # assigning function to a variable
        # def a(): print('test')
        # var=a
        # var()
        ####
        # >>> x._forms_[2].__class__
        # <class 'builtin_function_or_method'>
        # >>> x._forms_[1].__class__
        # <class 'float'>
        # >>> x._forms_[0].__class__
        # <class 'str'>

        self.__forms.append(item)


class LogFormatterNull(BLogFormatter):
    """Log Formatter Null class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)


class LogFormatterDateTime(BLogFormatter):
    """Log Formatter DateTime class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)


class LogFormatterTime(BLogFormatter):
    """Log Formatter Time class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)


class LogFormatterTimestamp(BLogFormatter):
    """Log Formatter Timestamp class."""

    def __init__(self):
        """Constructor."""
        BLogFormatter.__init__(self)


# #[EOF]#######################################################################
