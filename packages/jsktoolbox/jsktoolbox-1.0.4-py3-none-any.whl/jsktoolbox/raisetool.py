# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.05.2023

  Purpose: Raise class for formatting thrown exception messages.
  The message can be formatted with information about the class,
  method, and line number where the exception was thrown.
"""
from types import FrameType
from typing import Optional
from jsktoolbox.attribtool import NoDynamicAttributes


class Raise(NoDynamicAttributes):
    """Raise class for formatting thrown exception messages."""

    @classmethod
    def message(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> str:
        """Message formatter method.

        message: str    - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: formatted message string
        """
        template = f"{message}"
        if currentframe and isinstance(currentframe, FrameType):
            template = f"{currentframe.f_code.co_name} [line:{currentframe.f_lineno}]: {template}"
        elif isinstance(class_name, str) and class_name != "":
            template = f"{class_name}: {template}"
            return template
        else:
            return template
        template = f"{class_name}.{template}"
        return template

    @classmethod
    def attribute_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> AttributeError:
        """Return AttributeError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: AttributeError
        """
        return cls.error(message, AttributeError, class_name, currentframe)

    @classmethod
    def connection_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> ConnectionError:
        """Return ConnectionError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: ConnectionError
        """
        return cls.error(message, ConnectionError, class_name, currentframe)

    @classmethod
    def error(
        cls,
        message: str,
        exception: Exception = Exception,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> Exception:
        """Return exception with formatted string.

        message: str - message to format
        exception: Exception - custom exception to return
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: given exception type"""
        if isinstance(exception, type):
            if not isinstance(exception(), Exception):
                raise cls.error(
                    f"Exception class or its derived class expected, '{exception.__qualname__}' received.",
                    TypeError,
                    class_name,
                    currentframe,
                )
        else:
            raise cls.error(
                "Exception class or its derived class expected.",
                TypeError,
                class_name,
                currentframe,
            )
        return exception(
            cls.message(
                f"[{exception.__qualname__}]: {message}"
                if message
                else f"[{exception.__qualname__}]",
                class_name,
                currentframe,
            )
        )

    @classmethod
    def index_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> IndexError:
        """Return IndexError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: IndexError
        """
        return cls.error(message, IndexError, class_name, currentframe)

    @classmethod
    def key_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> KeyError:
        """Return KeyError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: KeyError
        """
        return cls.error(message, KeyError, class_name, currentframe)

    @classmethod
    def not_implemented_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> NotImplementedError:
        """Return NotImplementedError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: NotImplementedError
        """
        return cls.error(
            message, NotImplementedError, class_name, currentframe
        )

    @classmethod
    def os_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> OSError:
        """Return OSError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: OSError
        """
        return cls.error(message, OSError, class_name, currentframe)

    @classmethod
    def syntax_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> SyntaxError:
        """Return SyntaxError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: SyntaxError
        """
        return cls.error(message, SyntaxError, class_name, currentframe)

    @classmethod
    def type_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> TypeError:
        """Return TypeError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: TypeError
        """
        return cls.error(message, TypeError, class_name, currentframe)

    @classmethod
    def value_error(
        cls,
        message: str,
        class_name: str = "",
        currentframe: Optional[FrameType] = None,
    ) -> ValueError:
        """Return ValueError exception with formatted string.

        message: str - message to format
        class_name: str - caller class name (self.__class__.__name__)
        currentframe: FrameType - object from inspect.currentframe()

        Return: ValueError
        """
        return cls.error(message, ValueError, class_name, currentframe)


# #[EOF]#######################################################################
