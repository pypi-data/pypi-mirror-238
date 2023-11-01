# -*- coding: utf-8 -*-

"""
This module is used to debug ``zelfred`` library.
"""

from datetime import datetime
from .paths import path_log_txt


class Debugger:
    """
    This class is used to debug ``zelfred`` library.

    :param path_log_txt: the path to the log file.
    """
    def __init__(self):
        self.path_log_txt = path_log_txt
        self._enable = False

    def reset(self):
        """
        Remove the log file.
        """
        try:
            self.path_log_txt.unlink()
        except FileNotFoundError:
            pass

    def enable(self):
        """
        Enable the debugger.
        """
        self._enable = True

    def disable(self):
        """
        Disable the debugger.
        """
        self._enable = False

    def _log(self, text: str):
        with self.path_log_txt.open("a") as f:
            ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            line = f"{ts} {text}\n"
            f.write(line)

    def log(self, text: str):
        """
        Log (append a new line) a text to the log file.
        """
        if self._enable:
            self._log(text)


debugger = Debugger()
