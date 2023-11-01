# -*- coding: utf-8 -*-
"""
    pip_services4_observability.log.ConsoleLogger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Console logger implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import sys
from typing import Optional

from pip_services4_components.context.IContext import IContext
from pip_services4_components.context.ContextResolver import ContextResolver

from .LogLevel import LogLevel
from .LogLevelConverter import LogLevelConverter
from .Logger import Logger


class ConsoleLogger(Logger):
    """
    Logger that writes log messages to console.

    Errors are written to standard err stream and all other messages to standard out stream.

    ### Configuration parameters ###
        - level:             maximum log level to capture
        - source:            source (context) name

    ### References ###
        - `*:context-info:*:*:1.0`     (optional) :class:`ContextInfo <pip_services4_observability.info.ContextInfo.ContextInfo>` to detect the context id and specify counters source

    Example:

    .. code-block:: python

        logger = ConsoleLogger()
        logger.set_level(LogLevel.debug)

        logger.error(Context.from_trace_id("123"), ex, "Error occured: %s", ex.message)
        logger.debug(Context.from_trace_id("123"), "Everything is OK.")
    """

    def _write(self, level: LogLevel, context: Optional[IContext], error: Optional[Exception], message: Optional[str]):
        """
        Writes a log message to the logger destination.

        :param level: a log level.

        :param context: (optional) transaction id to trace execution through call chain.

        :param error: an error object associated with this message.

        :param message: a human-readable message to log.
        """
        if self._level < level:
            return

        output = "["
        output += ContextResolver.get_trace_id(context) if context is not None else "---"
        output += ":"
        output += LogLevelConverter.to_string(level)
        output += ":"
        output += datetime.datetime.utcnow().isoformat()
        output += "] "

        output += message

        if error is not None:
            if len(message) == 0:
                output += "Error: "
            else:
                output += ": "

            output += self._compose_error(error)

        output += "\n"

        if LogLevel.Fatal <= level <= LogLevel.Warn:
            sys.stderr.write(output)
        else:
            sys.stdout.write(output)
