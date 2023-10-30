# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-01 14:47:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Print methods.
"""


from typing import Any, Literal, Optional, ClassVar, Callable, Union
import sys
from io import TextIOWrapper
from os import devnull as os_devnull
from os.path import abspath as os_abspath

from .rsystem import get_first_notnull, get_name, rstack
from .rtext import to_text, add_text_frame


__all__ = (
    "RPrint",
    "rprint"
)


abspath_rprint = os_abspath(__file__)


class RPrint(object):
    """
    Rey's `print` type.
    """


    # State
    stoped: ClassVar[bool] = False
    modified: ClassVar[bool] = False

    # IO.
    io_null: ClassVar[TextIOWrapper] = open(os_devnull, "w")
    io_stdout: ClassVar[TextIOWrapper] = sys.stdout
    io_stdout_write: ClassVar[Callable[[str], int]] = sys.stdout.write

    # Frame type.
    frame_plain: ClassVar[bool] = False

    # Default value.
    default_width: ClassVar[int] = 100


    def beautify(
        self,
        *data: Any,
        title: Union[bool, str] = True,
        width: Optional[int] = None,
        frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full"
    ) -> str:
        """
        `Beautify` data to text.

        Parameters
        ----------
        data : Text data.
        title : Text title.
            - `Literal[True]` : Automatic get data variable name.
            - `Literal[False]` : No title.
            - `str` : Use this value as the title.

        width : Text width.
            - `None` : Use attribute `default_width`.
            - `int` : Use this value.

        frame : Text frame type.
            - `Literal[`full`]` : Add beautiful four side frame and limit length.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
                * When throw `exception`, then frame is `half` type.
            - `Literal[`half`]` : Add beautiful top and bottom side frame.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
            - `Literal[`top`]` : Add beautiful top side frame.
                * When attribute `frame_plain` is True, then frame is `top_plain` type.
            - `Literal[`half_plain`]` : Add plain top and bottom side frame.
            - `Literal[`top_plain`]` : Add plain top side frame.

        Returns
        -------
        Beautify text.
        """

        # Get parameter.

        ## Title.
        if title is True:
            titles = get_name(data)
            if titles is not None:
                titles = [title if title[:1] != "`" else "" for title in titles]
                if set(titles) != {""}:
                    title = " │ ".join(titles)
        if title.__class__ != str:
            title = None

        ## Width.
        width = get_first_notnull(width, self.default_width, default="exception")

        ## Frame.
        if self.frame_plain:
            if frame == "full":
                frame = "half_plain"
            elif frame == "half":
                frame = "half_plain"
            elif frame == "top":
                frame = "top_plain"

        # To text.
        text_list = [
            to_text(content, width=width)
            for content in data
        ]

        # Add frame.
        text = add_text_frame(*text_list, title=title, width=width, frame=frame)

        return text


    def rprint(
        self,
        *data: Any,
        title: Union[bool, str] = True,
        width: Optional[int] = None,
        frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full"
    ) -> str:
        """
        `Beautify` data to text, and `print`.

        Parameters
        ----------
        data : Text data.
        title : Text title.
            - `Literal[True]` : Automatic get data variable name.
            - `Literal[False]` : No title.
            - `str` : Use this value as the title.

        width : Text width.
            - `None` : Use attribute `default_width`.
            - `int` : Use this value.

        frame : Text frame type.
            - `Literal[`full`]` : Add beautiful four side frame and limit length.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
                * When throw `exception`, then frame is `half` type.
            - `Literal[`half`]` : Add beautiful top and bottom side frame.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
            - `Literal[`top`]` : Add beautiful top side frame.
                * When attribute `frame_plain` is True, then frame is `top_plain` type.
            - `Literal[`half_plain`]` : Add plain top and bottom side frame.
            - `Literal[`top_plain`]` : Add plain top side frame.

        Returns
        -------
        Beautify text.
        """

        # Beautify.
        text = self.beautify(*data, title=title, width=width, frame=frame)

        # Print.
        print(text)

        return text


    def rinput(
        self,
        *data: Any,
        title: Union[bool, str] = True,
        width: Optional[int] = None,
        frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full",
        extra: Optional[str] = None
    ) -> str:
        """
        `Beautify` data to text, and `print` data, and `read` string from standard input.

        Parameters
        ----------
        data : Text data.
        title : Text title.
            - `Literal[True]` : Automatic get data variable name.
            - `Literal[False]` : No title.
            - `str` : Use this value as the title.

        width : Text width.
            - `None` : Use attribute `default_width`.
            - `int` : Use this value.

        frame : Text frame type.
            - `Literal[`full`]` : Add beautiful four side frame and limit length.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
                * When throw `exception`, then frame is `half` type.
            - `Literal[`half`]` : Add beautiful top and bottom side frame.
                * When attribute `frame_plain` is True, then frame is `half_plain` type.
            - `Literal[`top`]` : Add beautiful top side frame.
                * When attribute `frame_plain` is True, then frame is `top_plain` type.
            - `Literal[`half_plain`]` : Add plain top and bottom side frame.
            - `Literal[`top_plain`]` : Add plain top side frame.

        extra : Extra print text at the end.

        Returns
        -------
        Standard input string.
        """

        # Beautify.
        text = self.beautify(*data, title=title, width=width, frame=frame)

        # Extra.
        if extra is not None:
            text += extra

        # Print.
        stdin = input(text)

        return stdin


    def stop(self) -> None:
        """
        Stop `standard output` print.
        """

        # Stop.
        sys.stdout = self.io_null

        # Update state.
        self.stoped = True


    def start(self) -> None:
        """
        Start `standard output` print.
        """

        # Check.
        if not self.stoped: return

        # Start.
        sys.stdout = self.io_stdout

        # Update state.
        self.stoped = False


    def modify(self, preprocess: Callable[[str], Optional[str]]) -> None:
        """
        Modify `standard output` print write method.

        Parameters
        ----------
        preprocess : Preprocess function.
            - `Callable[[str], str]` : Input old text, output new text, will trigger printing.
            - `Callable[[str], None]` : Input old text, no output, will not trigger printing.
        """


        # Define.
        def write(__s: str) -> Optional[int]:
            """
            Modified `standard output` write method.

            Parameters
            ----------
            """

            # Preprocess.
            __s = preprocess(__s)

            # Write.
            if __s.__class__ == str:
                write_len = self.io_stdout_write(__s)
                return write_len


        # Modify.
        self.io_stdout.write = write

        # Update state.
        self.modified = True


    def reset(self) -> None:
        """
        Reset `standard output` print write method.
        """

        # Check.
        if not self.modified: return

        # Reset.
        self.io_stdout.write = self.io_stdout_write

        # Update state.
        self.modified = False


    def add_position(self) -> None:
        """
        Add position text to `standard output`.
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

            # Break.
            if __s in ("\n", " ", "[0m"): return __s

            # Get parameter.
            stack_params = rstack.params
            stack_floor = stack_params[-1]

            ## Compatible "rprint".
            if (
                stack_floor["filename"] == abspath_rprint
                and stack_floor["name"] == "rprint"
            ):
                stack_floor = stack_params[-2]

            # Add.
            __s = 'File "%s", line %s\n%s' % (
                stack_floor["filename"],
                stack_floor["lineno"],
                __s
            )

            return __s


        # Modify.
        self.modify(preprocess)


    def __del__(self) -> None:
        """
        Delete handle.
        """

        # Start.
        self.start()

        # Reset.
        self.reset()


    __call__ = rprint


# Instance.

## Type "RPrint".
rprint = RPrint()