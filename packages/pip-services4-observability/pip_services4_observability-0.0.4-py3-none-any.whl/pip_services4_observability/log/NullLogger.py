# -*- coding: utf-8 -*-
"""
    pip_services4_observability.log.NullLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Null logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional, Any

from pip_services4_components.context.IContext import IContext

from .ILogger import ILogger
from .LogLevel import LogLevel


class NullLogger(ILogger):
    """
    Dummy implementation of logger that doesn't do anything.
    It can be used in testing or in situations when logger is required but shall be disabled.
    """

    def get_level(self) -> LogLevel:
        """
        Gets the maximum log level. Messages with higher log level are filtered out.

        :return: the maximum log level.
        """
        return LogLevel.Nothing

    def set_level(self, level: LogLevel):
        """
        Set the maximum log level.

        :param level: a new maximum log level.
        """
        pass

    def log(self, level: LogLevel, context: Optional[IContext], error: Optional[Exception], message: Optional[str],
            *args: Any,
            **kwargs: Any):
        """
        Logs a message at specified log level.

        :param level: a log level.

        :param context: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def fatal(self, context: Optional[IContext], error: Exception, message: str, *args: Any, **kwargs: Any):
        """
        Logs fatal (unrecoverable) message that caused the process to crash.

        :param context: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def error(self, context: Optional[IContext], error: Exception, message: str, *args: Any, **kwargs: Any):
        """
        Logs recoverable application error.

        :param context: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def warn(self, context: Optional[IContext], message: str, *args: Any, **kwargs: Any):
        """
        Logs a warning that may or may not have a negative impact.

        :param context: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def info(self, context: Optional[IContext], message: str, *args: Any, **kwargs: Any):
        """
        Logs an important information message

        :param context: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def debug(self, context: Optional[IContext], message: str, *args: Any, **kwargs: Any):
        """
        Logs a high-level debug information for troubleshooting.

        :param context: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass

    def trace(self, context: Optional[IContext], message: str, *args: Any, **kwargs: Any):
        """
        Logs a low-level debug information for troubleshooting.

        :param context: (optional) transaction id to trace execution through call chain.

        :param message: a human-readable message to log.

        :param args: arguments to parameterize the message.

        :param kwargs: arguments to parameterize the message.
        """
        pass
