# -*- coding: utf-8 -*-

"""
todo: doc string here
"""

import typing as T


class EndOfInputError(Exception):
    """
    todo: doc string here
    """

    def __init__(
        self,
        selection: T.Any,
        message: str = "End of input",
        *args,
    ):
        super().__init__(*args)
        self.selection = selection
        self.message = message


class JumpOutSessionError(Exception):
    """
    todo: doc string here
    """
    pass


JumpOutLoopError = JumpOutSessionError  # this is for backward compatibility


class TerminalTooSmallError(SystemError):
    """
    todo: doc string here
    """
    pass


class NoItemToSelectError(IndexError):
    """
    todo: doc string here
    """
    pass
