# -*- coding: utf-8 -*-

import typing as T


class EndOfInputError(Exception):
    """ """

    def __init__(
        self,
        selection: T.Any,
        message: str = "End of input",
        *args,
    ):
        super().__init__(*args)
        self.selection = selection
        self.message = message


class JumpOutLoopError(Exception):
    pass


class TerminalTooSmallError(SystemError):
    pass


class NoItemToSelectError(IndexError):
    pass
