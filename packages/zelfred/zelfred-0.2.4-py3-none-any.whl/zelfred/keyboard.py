# -*- coding: utf-8 -*-

from sys import platform

from readchar import key

UP = key.UP  # select the previous item in dropdown menu.
DOWN = key.DOWN  # select the next item in dropdown menu.
LEFT = key.LEFT  # move cursor
RIGHT = key.RIGHT  # move cursor

TAB = key.TAB  # auto complete
HOME = key.HOME  # move cursor to the beginning of the line
END = key.END  # move cursor to the end of the line
BACKSPACE = key.BACKSPACE  # delete previous character
DELETE = key.DELETE  # delete next character
ENTER = key.ENTER  # user action
CR = key.CR
LF = key.LF

CTRL_W = key.CTRL_W  # user action
CTRL_E = key.CTRL_E  # select the previous item in dropdown menu.
CTRL_R = key.CTRL_R  # scroll up
CTRL_T = key.CTRL_T  # user custom shortcut
CTRL_U = key.CTRL_U  # user action
CTRL_P = key.CTRL_P  # user action
CTRL_A = key.CTRL_A  # user action
CTRL_D = key.CTRL_D  # select the next item in dropdown menu.
CTRL_F = key.CTRL_F  # scroll down
CTRL_G = key.CTRL_G  # user custom shortcut
CTRL_H = key.CTRL_H  # DON'T USE THIS, IT DOESN'T WORK ON WINDOWS
CTRL_K = key.CTRL_K  # delete previous word
CTRL_L = key.CTRL_L  # delete next word
CTRL_X = key.CTRL_X  # clear the user input.
CTRL_C = key.CTRL_C  # keyboard interrupt
CTRL_B = key.CTRL_B  # user custom shortcut
CTRL_N = key.CTRL_N  # user custom shortcut


if platform.startswith(("linux", "darwin", "freebsd")):
    ALT_LEFT = "\x1bb"  # move to previous word
    ALT_RIGHT = "\x1bf"  # move to next word
elif platform in ("win32", "cygwin"):
    ALT_LEFT = "\x00\x9b"  # move to previous word
    ALT_RIGHT = "\x00\x9d"  # move to next word
else:
    raise NotImplementedError(f"The platform {platform} is not supported yet")


# Looks like it doesn't work on windows.
# ALT_Q = "œ"
# ALT_W = "∑"
# ALT_R = "®"
# ALT_T = "†"
# ALT_O = "ø"
# ALT_P = "π"
# ALT_A = "å"
# ALT_S = "ß"
# ALT_D = "∂"
# ALT_F = "ƒ"
# ALT_G = "©"
# ALT_H = "˙"
# ALT_J = "∆"
# ALT_K = "˚"
# ALT_L = "¬"
# ALT_Z = "Ω"
# ALT_X = "≈"
# ALT_C = "ç"
# ALT_V = "√"
# ALT_B = "∫"
# ALT_M = "µ"

F1 = key.F1  # Jump out the sub-session, return to the previous view.
F2 = key.F2
F3 = key.F3
F4 = key.F4
F5 = key.F5
F6 = key.F6
F7 = key.F7
F8 = key.F8
F9 = key.F9
F10 = key.F10
F11 = key.F11
F12 = key.F12

key_code_to_name_mapper = {
    UP: "UP",
    DOWN: "DOWN",
    LEFT: "LEFT",
    RIGHT: "RIGHT",
    TAB: "TAB",
    HOME: "HOME",
    END: "END",
    BACKSPACE: "BACKSPACE",
    DELETE: "DELETE",
    ENTER: "ENTER",
    CR: "CR",
    LF: "LF",
    CTRL_W: "CTRL_W",
    CTRL_E: "CTRL_E",
    CTRL_R: "CTRL_R",
    CTRL_T: "CTRL_T",
    CTRL_U: "CTRL_U",
    CTRL_P: "CTRL_P",
    CTRL_A: "CTRL_A",
    CTRL_D: "CTRL_D",
    CTRL_F: "CTRL_F",
    CTRL_G: "CTRL_G",
    CTRL_H: "CTRL_H",
    CTRL_K: "CTRL_K",
    CTRL_L: "CTRL_L",
    CTRL_X: "CTRL_X",
    CTRL_B: "CTRL_B",
    CTRL_N: "CTRL_N",
    ALT_LEFT: "ALT_LEFT",
    ALT_RIGHT: "ALT_RIGHT",
    # ALT_Q: "ALT_Q",
    # ALT_W: "ALT_W",
    # ALT_R: "ALT_R",
    # ALT_T: "ALT_T",
    # ALT_O: "ALT_O",
    # ALT_P: "ALT_P",
    # ALT_A: "ALT_A",
    # ALT_S: "ALT_S",
    # ALT_D: "ALT_D",
    # ALT_F: "ALT_F",
    # ALT_G: "ALT_G",
    # ALT_H: "ALT_H",
    # ALT_J: "ALT_J",
    # ALT_K: "ALT_K",
    # ALT_L: "ALT_L",
    # ALT_Z: "ALT_Z",
    # ALT_X: "ALT_X",
    # ALT_C: "ALT_C",
    # ALT_V: "ALT_V",
    # ALT_B: "ALT_B",
    # ALT_M: "ALT_M",
    F1: "F1",
    F2: "F2",
    F3: "F3",
    F4: "F4",
    F5: "F5",
    F6: "F6",
    F7: "F7",
    F8: "F8",
    F9: "F9",
    F10: "F10",
    F11: "F11",
    F12: "F12",
}


def get_key_name_by_code(code: str) -> str:
    return key_code_to_name_mapper[code]
