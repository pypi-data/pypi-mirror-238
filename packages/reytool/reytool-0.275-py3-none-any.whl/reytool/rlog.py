# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-08 21:26:43
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Log methods.
"""


from __future__ import annotations
from typing import Any, Tuple, Dict, Optional, Union, Literal, Final, Callable, ClassVar, NoReturn, overload
from queue import Queue
from os.path import abspath as os_abspath
from re import sub as re_sub
from logging import getLogger, Handler, StreamHandler, FileHandler, Formatter, Filter, LogRecord, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import QueueHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler, ConcurrentTimedRotatingFileHandler

from .rprint import rprint, abspath_rprint
from .rregular import search
from .rsystem import get_first_notnull, rexc, rstack
from .rtext import to_text
from .rtime import now, time_to
from .rwrap import start_thread


__all__ = (
    "RLog",
)


abspath_rlog = os_abspath(__file__)


class RLog(object):
    """
    Rey's `log` type.
    """

    # State
    print_replaced: ClassVar[bool] = False

    # Default value.
    default_format: ClassVar[str] = (
        "%(time_format)s | "
        "%(levelname_format)s | "
        "%(path_format)s | "
        "%(message_format)s"
    )
    default_format_date: ClassVar[str] = "%Y-%m-%d %H:%M:%S"
    default_format_width: ClassVar[int] = 100


    def __init__(
        self,
        name: str = "Log"
    ) -> None:
        """
        Build `log` instance.

        Parameters
        ----------
        name : Log name. When log name existed, then direct return, otherwise build.
        """

        # Set attribute.
        self.name: Final[str] = name
        self.stoped = False

        # Get logger.
        self.logger = getLogger(name)

        # Set level.
        self.logger.setLevel(DEBUG)


    def _get_message_stack(self) -> Dict:
        """
        Get message stack parameters.

        Returns
        -------
        Stack parameters.
        """

        # Get parameter.
        stack_params = rstack.get_stack_param("full", 12)
        stack_param = stack_params[-1]

        # Compatible.

        ## Compatible "__call__".
        if (
            stack_param["filename"] == abspath_rlog
            and stack_param["name"] in ("debug", "info", "warning", "error", "critical")
        ):
            stack_param = stack_params[-2]

        ## Compatible "print".
        if (
            stack_param["filename"] == abspath_rlog
            and stack_param["name"] == "preprocess"
        ):
            stack_param = stack_params[-3]

        ## Compatible "rprint".
        if (
            stack_param["filename"] == abspath_rprint
            and stack_param["name"] == "rprint"
        ):
            stack_param = stack_params[-4]

        return stack_param


    def _supply_format_standard(
        self,
        format_: str,
        record: LogRecord
    ) -> None:
        """
        Supply format standard parameters.

        Parameters
        ----------
        format_ : Record format.
        record : Log record instance.
        """

        # Format "time_format".
        if "%(time_format)s" in format_:
            datetime = now()
            datetime_str = time_to(datetime, True)
            record.time_format = datetime_str[:-3]

        # Format "levelname_format".
        if "%(levelname_format)s" in format_:
            record.levelname_format = record.levelname.ljust(8)

        # Format "path_format".
        if "%(path_format)s" in format_:
            message_stack = self._get_message_stack()
            record.path_format = "%s:%s" % (
                message_stack["filename"],
                message_stack["lineno"]
            )

        # Format "message_format".
        if "%(message_format)s" in format_:
            record.message_format = record.getMessage()


    def _get_level_color_ansi(
        self,
        level: int
    ) -> str:
        """
        Get level color `ANSI` code.

        Parameters
        ----------
        level : Record level.

        Returns
        -------
        Level color ansi code.
        """

        # Set parameters.
        color_code_dict = {
            10: "\033[1;34m",
            20: "\033[1;37m",
            30: "\033[1;33m",
            40: "\033[1;31m",
            50: "\033[1;37;41m"
        }

        # Get.
        color_code = color_code_dict.get(level, "")

        return color_code


    def _supply_format_print(
        self,
        format_: str,
        record: LogRecord
    ) -> None:
        """
        Supply format print parameters.

        Parameters
        ----------
        format_ : Record format.
        record : Log record instance.
        """

        # Format color.
        result = search("\033\[[\d;]+?m", format_)
        if result is None:

            # "time_format".
            if "%(time_format)s" in format_:
                record.time_format = "\033[32m%s\033[0m" % record.time_format

            # "levelname_format".
            if "%(levelname_format)s" in format_:
                level_color_code = self._get_level_color_ansi(record.levelno)
                record.levelname_format = "%s%s\033[0m" % (
                    level_color_code,
                    record.levelname_format
                )

            # "path_format".
            if "%(path_format)s" in format_:
                record.path_format = "\033[36m%s\033[0m" % record.path_format

            # "message_format".
            if (
                "%(message_format)s" in format_
                and search("\033\[[\d;]+?m", record.message_format) is None
            ):
                level_color_code = self._get_level_color_ansi(record.levelno)
                record.message_format = "%s%s\033[0m" % (
                    level_color_code,
                    record.message_format
                )


    def _supply_format_file(
        self,
        format_: str,
        record: LogRecord
    ) -> None:
        """
        Supply format file parameters.

        Parameters
        ----------
        format_ : Record format.
        record : Log record instance.
        """

        # Format "message_format".
        if "%(message_format)s" in format_:
            pattern = "\033\[[\d;]+?m"
            record.message_format = re_sub(pattern, "", record.message_format)


    def get_default_filter_method(
        self,
        format_: str,
        type_ : Optional[Literal["print", "file"]] = None
    ) -> Callable[[LogRecord], Literal[True]]:
        """
        Get default filter method of handler.

        Parameters
        ----------
        format_ : Record format.
        type_ : Handler type.
            - `None` : Standard filter method.
            - `Literal['print'] : Print handler filter method.
            - `Literal['file'] : File handler filter method.

        Returns
        -------
        Filter method.
        """


        # Define.
        def default_filter_method(
            record: LogRecord
        ) -> Literal[True]:
            """
            Default filter method of handler.

            Parameters
            ----------
            record : Log record instance.

            Returns
            -------
            Whether pass.
            """

            # Format standard.
            self._supply_format_standard(format_, record)

            # Format print.
            if type_ == "print":
                self._supply_format_print(format_, record)

            # Format file.
            elif type_ == "file":
                self._supply_format_file(format_, record)

            return True


        return default_filter_method


    def get_filter(
        self,
        method: Callable[[LogRecord], bool]
    ) -> Filter:
        """
        Get filter.

        Parameters
        ----------
        method : Filter method.

        Returns
        -------
        Filter.
        """


        # Define.
        class RFilter(Filter):
            """
            Rey's filter type.
            """


            def filter(
                record: LogRecord
            ) -> Literal[True]:
                """
                Filter method.

                Parameters
                ----------
                record : Log record instance.

                Returns
                -------
                Whether pass.
                """

                # Filter.
                result = method(record)

                return result


        return RFilter


    def add_print(
        self,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> StreamHandler:
        """
        Add print output record handler.

        Parameters
        ----------
        level : Handler level.
        format_ : Record format.
            - `None` : Use attribute `default_format`.
            - `str` : Use this value. 
                * `Contain 'time_format'` : Date and time and millisecond, print output with color.
                * `Contain 'levelname_format'` : Level name and fixed width, print output with color.
                * `Contain 'path_format'` : Record code path, print output with color.
                * `Contain 'message_format'` : message content, file output delete ANSI code, print outputwith color.

        filter_ : Filter method. The parameter is the `LogRecord` instance, return is `bool`.
            - `None` : Use default filter method.
            - `Callable` : Use this method.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format, default="exception")
        if filter_ is None:
            filter_ = self.get_default_filter_method(format_, "print")

        # Create handler.
        handler = StreamHandler()
        handler.setLevel(level)
        formatter = Formatter(format_, self.default_format_date)
        handler.setFormatter(formatter)
        handler_filter = self.get_filter(filter_)
        handler.addFilter(handler_filter)

        # Add.
        self.logger.addHandler(handler)

        return handler


    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: Optional[float] = None,
        time: None = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> ConcurrentRotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: None = None,
        time: Union[float, Literal["m", "w0", "w1", "w2", "w3", "w4", "w5", "w6"]] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> ConcurrentTimedRotatingFileHandler: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: None = None,
        time: Any = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> NoReturn: ...

    @overload
    def add_file(
        self,
        path: Optional[str] = None,
        mb: float = None,
        time: Union[float, Literal["m", "w0", "w1", "w2", "w3", "w4", "w5", "w6"]] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> NoReturn: ...

    def add_file(
        self,
        path: Optional[str] = None,
        mb: Optional[float] = None,
        time: Optional[Union[float, Literal["m", "w0", "w1", "w2", "w3", "w4", "w5", "w6"]]] = None,
        level: int = DEBUG,
        format_: Optional[str] = None,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> Union[ConcurrentRotatingFileHandler, ConcurrentTimedRotatingFileHandler]:
        """
        Add file output record handler, can split files based on size or time.

        Parameters
        ----------
        path : File path.
            - `None` : Use attribute `self.name`.
            - `str` : Use this value.

        mb : File split condition, max megabyte. Conflict with parameter `time`. Cannot be less than 1, prevent infinite split file.
        time : File split condition, interval time. Conflict with parameter `mb`.
            - `float` : Interval hours.
            - `Literal['m']` : Everyday midnight.
            - `Literal['w0', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6']` : Weekly midnight, 'w0' is monday, 'w6' is sunday, and so on.

        level : Handler level.
        format_ : Record format.
            - `None` : Use attribute `default_format`.
            - `str` : Use this value.
                * `Contain 'time_format'` : Date and time and millisecond, print output with color.
                * `Contain 'levelname_format'` : Level name and fixed width, print output with color.
                * `Contain 'path_format'` : Record code path, print output with color.
                * `Contain 'message_format'` : message content, file output delete ANSI code, print outputwith color.

        filter_ : Filter method. The parameter is the `LogRecord` instance, return is `bool`.
            - `None` : Use default filter method.
            - `Callable` : Use this method.

        Returns
        -------
        Handler.
        """

        # Get parameter.
        format_ = get_first_notnull(format_, self.default_format, default="exception")
        if path is None:
            path = self.name
        if filter_ is None:
            filter_ = self.get_default_filter_method(format_, "file")

        # Create handler.

        ## Raise.
        if (
            mb is not None
            and time is not None
        ):
            raise AssertionError("parameter 'mb' and 'time' cannot be used together")

        ## By size split.
        elif mb is not None:

            ### Check.
            # if mb < 1:
            #     rexc(ValueError, mb)

            byte = int(mb * 1024 * 1024)
            handler = ConcurrentRotatingFileHandler(
                path,
                "a",
                byte,
                1_0000_0000,
                delay=True
            )

        ## By time split.
        elif time is not None:

            ### Interval hours.
            if time.__class__ in (int, float):
                second = int(time * 60 * 60)
                handler = ConcurrentTimedRotatingFileHandler(
                    path,
                    "S",
                    second,
                    1_0000_0000,
                    delay=True
                )

            ### Everyday midnight.
            elif time == "m":
                handler = ConcurrentTimedRotatingFileHandler(
                    path,
                    "MIDNIGHT",
                    backupCount=1_0000_0000,
                    delay=True
                )

            ### Weekly midnight
            elif time in ("w0", "w1", "w2", "w3", "w4", "w5", "w6"):
                handler = ConcurrentTimedRotatingFileHandler(
                    path,
                    time,
                    backupCount=1_0000_0000,
                    delay=True
                )

            ### Raise.
            else:
                rexc(ValueError, time)

        ## Not split.
        else:
            handler = ConcurrentRotatingFileHandler(
                path,
                "a",
                delay=True
            )

        # Set handler.
        handler.setLevel(level)
        formatter = Formatter(format_, self.default_format_date)
        handler.setFormatter(formatter)
        handler_filter = self.get_filter(filter_)
        handler.addFilter(handler_filter)

        # Add.
        self.logger.addHandler(handler)

        return handler


    def add_queue(
        self,
        queue: Optional[Queue] = None,
        level: int = DEBUG,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> Tuple[QueueHandler, Queue[LogRecord]]:
        """
        Add queue output record handler.

        Parameters
        ----------
        queue : Queue instance.
            - `None` : Create queue and use.
            - `Queue` : Use this queue.

        level : Handler level.
        filter_ : Filter method. The parameter is the `LogRecord` instance, return is `bool`.

        Returns
        -------
        Handler and queue.
        """

        ## Create queue.
        if queue is None:
            queue = Queue()

        # Create handler.
        handler = QueueHandler(queue)

        # Set handler.
        handler.setLevel(level)
        if filter_ is not None:
            handler_filter = self.get_filter(filter_)
            handler.addFilter(handler_filter)

        # Add.
        self.logger.addHandler(handler)

        return handler, queue


    def add_handler(
        self,
        method: Callable[[LogRecord], Any],
        level: int = DEBUG,
        filter_: Optional[Callable[[LogRecord], bool]] = None
    ) -> None:
        """
        Add method record handler.

        Parameters
        ----------
        method : Handler method. The parameter is the `LogRecord` instance.
        level : Handler level.
        filter_ : Filter method. The parameter is the `LogRecord` instance, return is `bool`.
        """

        # Add queue out.
        _, queue = self.add_queue(level=level, filter_=filter_)


        # Define.
        @start_thread
        def execute() -> None:
            """
            Execute method.
            """

            while True:
                record = queue.get()
                method(record)


        # Execute.
        execute()


    def delete_handler(self, handler: Optional[Handler] = None) -> None:
        """
        Delete record handler.

        Parameters
        ----------
        handler : Handler.
            - `None` : Delete all handler.
            - `Handler` : Delete this handler.
        """

        # Delete.

        ## This.
        if handler is None:
            for handle in self.logger.handlers:
                self.logger.removeHandler(handle)

        ## All.
        else:
            self.logger.removeHandler(handler)


    def catch_print(self, printing: bool = True) -> None:
        """
        Catch print to log.

        Parameters
        ----------
        printing : Whether to still print.
        """


        # Define.
        def preprocess(__s: str) -> str:
            """
            Preprocess function.

            Parameters
            ----------
            __s : Standard ouput text.

            Returns
            -------
            Preprocessed text.
            """

            # Log.
            if __s not in ("\n", " ", "[0m"):
                self(__s)

            # Print.
            if printing:
                return __s


        # Modify.
        rprint.modify(preprocess)

        # Update state.
        self.print_replaced = True


    def reset_print(self) -> None:
        """
        Reset log replace print.
        """

        # Break.
        if not self.print_replaced: return

        # Reset.
        rprint.reset()

        # Update state.
        self.print_replaced = False


    def log(
        self,
        *messages: Optional[Any],
        level: Optional[int] = None
    ) -> None:
        """
        Record log.

        Parameters
        ----------
        messages : Record content.
        level : Record level.
            - `None` : Automatic judge.
                * `in 'except' syntax` : Use 'ERROR' level.
                * `Other` : Use 'INFO' level.
            - `int` : Use this value.
        """

        # Get parameter.

        ## Messages.
        messages_len = len(messages)
        if messages_len == 0:
            messages = [None]

        ## Level.
        _, exc_type, _, _ = rexc.catch()
        if level is None:
            if exc_type is None:
                level = INFO
            else:
                level = ERROR

        # Convert.

        ## Join.
        messages = "\n".join(
            [
                to_text(message, self.default_format_width)
                for message in messages
            ]
        )
        if "\n" in messages:
            messages = "\n" + messages

        ## Exception.
        exc_stack, exc_type, _, _ = rexc.catch()
        if exc_type is not None:
            messages = "%s\n%s" % (
                messages,
                exc_stack
            )

        # Record.
        self.logger.log(level, messages)


    def debug(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `debug` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=DEBUG)


    def info(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `info` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=INFO)


    def warning(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `warning` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=WARNING)


    def error(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `error` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=ERROR)


    def critical(
        self,
        *messages: Optional[Any]
    ) -> None:
        """
        Record `critical` level log.

        Parameters
        ----------
        messages : Record content.
        """

        # Record.
        self.log(*messages, level=CRITICAL)


    def stop(self) -> None:
        """
        Stop record.
        """

        # Set level.
        self.logger.setLevel(100)

        # Update state.
        self.stoped = True


    def start(self) -> None:
        """
        Start record.
        """

        # Set level.
        self.logger.setLevel(DEBUG)

        # Update state.
        self.stoped = False


    def __del__(self) -> None:
        """
        Delete handle.
        """

        # Reset.
        self.reset_print()

        # Delete handler.
        self.delete_handler()


    __call__ = log