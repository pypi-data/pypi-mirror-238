# -*- coding: utf-8 -*-

"""
This module implements the key pressed event processing logics.
"""

import typing as T

from . import keyboard
from . import exc

if T.TYPE_CHECKING:
    from .item import T_ITEM
    from .ui import UI


class UIProcessKeyPressedMixin:
    """

    **Important**

    All methods whose names start with ``process_`` are abstract methods
    that handle specific key press events. They implement the Default behavior:.
    Experienced developers can override them to customize the behavior.
    """

    def cursor_up_and_down(self: "UI"):
        self.need_run_handler: bool = False
        self.need_clear_query: bool = False
        self.need_print_query: bool = False

    def wait_next_user_input(self: "UI"):
        self.need_run_handler = False
        self.need_move_to_end = False
        self.need_clear_items = False
        self.need_clear_query = False
        self.need_print_query = False
        self.need_print_items = False

    def cursor_left_and_right(self: "UI"):
        self.wait_next_user_input()

    def process_up(self: "UI"):
        """
        Default behavior:

        select the previous item in dropdown menu.
        """
        self.cursor_up_and_down()
        self.dropdown.press_up()

    def process_down(self: "UI"):
        """
        Default behavior:

        select the next item in dropdown menu.
        """
        self.cursor_up_and_down()
        self.dropdown.press_down()

    def process_ctrl_e(self: "UI"):
        """
        Default behavior:

        select the previous item in dropdown menu.
        """
        self.cursor_up_and_down()
        self.dropdown.press_up()

    def process_ctrl_d(self: "UI"):
        """
        Default behavior:

        select the next item in dropdown menu.
        """
        self.cursor_up_and_down()
        self.dropdown.press_down()

    def process_ctrl_r(self: "UI"):
        """
        Default behavior:

        scroll up the dropdown menu (press UP 5 times).
        """
        self.cursor_up_and_down()
        self.dropdown.scroll_up()

    def process_ctrl_f(self: "UI"):
        """
        Default behavior:

        scroll down the dropdown menu (press DOWN 5 times).
        """
        self.cursor_up_and_down()
        self.dropdown.scroll_down()

    def process_left(self: "UI"):
        """
        Default behavior:

        move user input cursor to the previous character.
        """
        self.cursor_left_and_right()
        self.line_editor.press_left()

    def process_right(self: "UI"):
        """
        Default behavior:

        move user input cursor to the next character.
        """
        self.cursor_left_and_right()
        self.line_editor.press_right()

    def process_alt_left(self: "UI"):
        """
        Default behavior:

        Move cursor to the beginning of previous word.
        """
        self.cursor_left_and_right()
        self.line_editor.move_word_backward()

    def process_alt_right(self: "UI"):
        """
        Default behavior:

        Move cursor to the beginning of next word.
        """
        self.cursor_left_and_right()
        self.line_editor.move_word_forward()

    def process_home(self: "UI"):
        """
        Default behavior:

        Move cursor to the beginning of the line.
        """
        self.cursor_left_and_right()
        self.line_editor.press_home()

    def process_end(self: "UI"):
        """
        Default behavior:

        Move cursor to the end of the line.
        """
        self.cursor_left_and_right()
        self.line_editor.press_end()

    def press_backspace(self: "UI"):
        """
        Default behavior:

        Delete character backwards in the line editor. Also move cursor to the left.
        """
        self.line_editor.press_backspace()

    def press_delete(self: "UI"):
        """
        Default behavior:

        Delete character forwards in the line editor. Also, the cursor stays.
        """
        self.line_editor.press_delete()

    def process_ctrl_k(self: "UI"):
        """
        Default behavior:

        Delete the previous word.
        """
        self.line_editor.delete_word_backward()

    def process_ctrl_l(self: "UI"):
        """
        Default behavior:

        Delete the next word.
        """
        self.line_editor.delete_word_forward()

    def process_tab(self: "UI"):
        """
        Default behavior:

        Auto complete.
        """
        self.line_editor.clear_line()
        selected_item = self.dropdown.selected_item
        if selected_item.autocomplete:
            self.line_editor.enter_text(selected_item.autocomplete)

    def process_ctrl_x(self: "UI"):
        """
        Default behavior:

        Clear the user input.
        """
        self.line_editor.clear_line()

    def process_ctrl_c(self: "UI"):
        """
        Default behavior:

        Keyboard interrupt.
        """
        raise KeyboardInterrupt()

    def validate_selected_item(self: "UI") -> T.Optional["T_ITEM"]:
        if self.dropdown.n_items == 0:
            raise exc.EndOfInputError(
                selection="select nothing",
            )
        else:
            self.move_to_end()
            if self.dropdown.items:
                return self.dropdown.selected_item
        return None

    def process_enter(self: "UI"):
        """
        Default behavior:

        User action for enter.
        """
        selected_item = self.validate_selected_item()
        if selected_item is not None:
            selected_item.enter_handler(ui=self)
            selected_item.post_enter_handler(ui=self)

    def process_ctrl_a(self: "UI"):
        """
        Default behavior:

        User action for CTRL A.
        """
        selected_item = self.validate_selected_item()
        if selected_item is not None:
            selected_item.ctrl_a_handler(ui=self)
            selected_item.post_ctrl_a_handler(ui=self)

    def process_ctrl_w(self: "UI"):
        """
        Default behavior:

        User action for CTRL W.
        """
        selected_item = self.validate_selected_item()
        if selected_item is not None:
            selected_item.ctrl_w_handler(ui=self)
            selected_item.post_ctrl_w_handler(ui=self)

    def process_ctrl_u(self: "UI"):
        """
        Default behavior:

        User action for CTRL U.
        """
        selected_item = self.validate_selected_item()
        if selected_item is not None:
            selected_item.ctrl_u_handler(ui=self)
            selected_item.post_ctrl_u_handler(ui=self)

    def process_ctrl_p(self: "UI"):
        """
        Default behavior:

        User action for CTRL P.
        """
        selected_item = self.validate_selected_item()
        if selected_item is not None:
            selected_item.ctrl_p_handler(ui=self)
            selected_item.post_ctrl_p_handler(ui=self)

    def process_f1(self: "UI"):
        """
        Default behavior:

        Jump out the sub-session, return to the previous view.
        """
        raise exc.JumpOutLoopError

    def _create_key_processor_mapper(self):
        self._key_processor_mapper = {
            # dropdown menu
            keyboard.UP: self.process_up,
            keyboard.DOWN: self.process_down,
            keyboard.CTRL_E: self.process_ctrl_e,
            keyboard.CTRL_D: self.process_ctrl_d,
            keyboard.CTRL_R: self.process_ctrl_r,
            keyboard.CTRL_F: self.process_ctrl_f,
            # line editor - move cursor
            keyboard.LEFT: self.process_left,
            keyboard.RIGHT: self.process_right,
            keyboard.ALT_LEFT: self.process_alt_left,
            keyboard.ALT_RIGHT: self.process_alt_right,
            keyboard.HOME: self.process_home,
            keyboard.END: self.process_end,
            # line editor - change text
            keyboard.BACKSPACE: self.press_backspace,
            keyboard.DELETE: self.press_delete,
            keyboard.CTRL_K: self.process_ctrl_k,
            keyboard.CTRL_L: self.process_ctrl_l,
            keyboard.TAB: self.process_tab,
            keyboard.CTRL_X: self.process_ctrl_x,
            # special
            keyboard.CTRL_C: self.process_ctrl_c,
            keyboard.ENTER: self.process_enter,
            keyboard.CTRL_A: self.process_ctrl_a,
            keyboard.CTRL_W: self.process_ctrl_w,
            keyboard.CTRL_P: self.process_ctrl_p,
            keyboard.F1: self.process_f1,
        }

    def _process_key_pressed_input(self: "UI", key: str):
        """
        Try to process the key pressed

        :return: a boolean flag indicating whether the key pressed is processed
        """
        if key in self._key_processor_mapper:
            self._key_processor_mapper[key]()
        else:
            self.line_editor.press_key(key)
