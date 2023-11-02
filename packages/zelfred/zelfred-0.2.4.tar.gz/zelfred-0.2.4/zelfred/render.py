# -*- coding: utf-8 -*-

"""
This module implements the render logic of the terminal UI.
"""

import typing as T
import dataclasses
import sys

from blessed import Terminal

from .item import T_ITEM
from .line_editor import LineEditor
from .dropdown import Dropdown
from .exc import TerminalTooSmallError


@dataclasses.dataclass
class Render:
    """
    Generic UI render. It can print string, print line, clear line, and move
    cursor up and down.

    :param terminal: blessed terminal object.
    :param line_number: store the current line number of the cursor.
        if 0, means it is at the first line.
        if 1, means it is at the second line.
    :param n_lines: store the total number of printed lines in the terminal.
    """

    terminal: Terminal = dataclasses.field(default_factory=Terminal)
    line_number: int = dataclasses.field(default=0)
    n_lines: int = dataclasses.field(default=0)

    def __post_init__(self):
        pass

    def _debug(self):  # pragma: no cover
        print(f"line_number = {self.line_number}")
        print(f"n_lines = {self.n_lines}")

    def print_str(
        self,
        str_tpl: str,
        new_line=False,
        **kwargs,
    ) -> str:
        """
        打印一个字符串, 可以选择是否换行. 并且自动更新 line_number 的值.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认不会.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        if new_line:
            self.line_number += 1
            self.n_lines += 1
        content = str_tpl.format(**kwargs)
        print(content, end="\n" if new_line else "")
        sys.stdout.flush()
        return content

    def print_line(
        self,
        str_tpl: str,
        new_line: bool = True,
        **kwargs,
    ) -> str:
        """
        打印一行, 默认自动换行.

        :param str_tpl: string template, 一个字符串模板.
        :param new_line: 如果是 True, 那么会自动换行, 否则不会. 默认自动换行.
        :param kwargs: 额外的传递给 str_tpl 的参数.
        """
        return self.print_str(
            str_tpl + self.terminal.clear_eol(),
            new_line=new_line,
            **kwargs,
        )

    def _force_initial_column(self) -> str:
        """
        用回车符 (注意! 不是换行符) 把光标移动到本行初始位置.
        """
        return self.print_str("\r")

    def move_to_start(self) -> int:  # pragma: no cover
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        n = self.line_number
        if n:
            print(n * self.terminal.move_up, end="")
        print("\r", end="")
        sys.stdout.flush()
        self.line_number = 0
        return n

    def move_up(self, n: int):  # pragma: no cover
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        print(n * self.terminal.move_up, end="")
        sys.stdout.flush()
        self.line_number -= n

    def move_down(self, n: int):  # pragma: no cover
        """
        把光标移动到初始位置. 本质上是把光标向上回退移动到第一行, 然后再用回车符把光标移动到本行初始位置.
        """
        print(n * self.terminal.move_down, end="")
        sys.stdout.flush()
        self.line_number += n

    def clear_n_lines(self, n: int):  # pragma: no cover
        """
        把光标以上的 n 行清空, 并把光标移动到行首. 常用于清除掉已经打印过的内容.
        """
        if n > self.line_number:
            raise ValueError
        for _ in range(n):
            print(self.terminal.move_up, end="")
            print(self.terminal.clear_eol(), end="")
            print(self.terminal.clear_bol(), end="")
        self._force_initial_column()
        self.line_number -= n
        self.n_lines -= n

    def clear_all(self):
        """
        清除所有内容, 并把光标移动到行首.

        Clear
        """
        self.clear_n_lines(n=self.line_number)

    @property
    def width(self):
        return self.terminal.width or 80

    @property
    def height(self):
        return self.terminal.width or 24


@dataclasses.dataclass
class UIRender(Render):
    """
    The Terminal UI Render. It extends the :class:`Render` class and highly
    optimized for the ``zelfred`` terminal UI layout.

    See below example, ``|`` represents the cursor:

    .. code-block::

        (Query): user query here|
        [x] item 1 title here
              item 1 subtitle here
        [ ] item 2 title here
              item 2 subtitle here
        [ ] item 3 title here
              item 3 subtitle here

    The first line ``(Query): user query here|`` is the user input box, it always
    starts with ``(Query): ``, and user can enter any text input after that.
    The cursor cannot go beyond the ``: `` part.

    User can use ``Left``, ``Right``, ``Backspace`` and ``Delete`` keys to edit the
    user input box.

    Below the first line is the items drop down menu. Each item has two lines.

    The first line is the title, it always starts with ``[x] `` or ``[ ] ``.
    ``[x] `` means the item is selected, ``[ ] `` means the item is not selected.
    You can only select one item at a time, and by default the first item is selected.
    There always be one item selected.

    The second line is the subtitle, it has 2 indent spaces comparing to the title.

    User can use the ``UP`` and ``DOWN`` keys to navigate the items drop down menu.

    The dropdown menu can show up to 10 items at a time, if the dropdown menu
    has more than 10 items, user can scroll down to see the rest of the items using
    the ``DOWN`` key. The ``CTRL + UP`` and ``CTRL + DOWN`` key can scroll up and down
    10 items at a time.
    """

    prompt: str = dataclasses.field(default="(Query)")
    checked_mark: str = dataclasses.field(default="[x]")
    not_checked_mark: str = dataclasses.field(default="[ ]")
    subtitle_pad: str = dataclasses.field(default=" " * 6)

    def __post_init__(self):
        super().__post_init__()

    # --------------------------------------------------------------------------
    # line editor
    # --------------------------------------------------------------------------
    def print_line_editor(
        self,
        line_editor: LineEditor,
    ) -> str:  # pragma: no cover
        """
        Render the line editor, the ``(Query): user query here|`` part. And move
        the cursor to the beginning of the next line, so it's ready to print the
        dropdown menu.

        It assumes that there is nothing in the terminal UI before running this.

        :param line_editor: the new :class:`~zelfred.line_editor.LineEditor` object.

        :return: text of the line editor.
        """

        return self.print_line(
            "{t.bold}{t.cyan}{prompt}: {t.normal}{line_editor.line}",
            prompt=self.prompt,
            line_editor=line_editor,
            t=self.terminal,
        )

    def clear_line_editor(self):  # pragma: no cover
        """
        Clear the line editor (the query input box at the first line).
        It doesn't require to move the cursor to the beginning of the line editor
        before calling this function, it will handle that automatically.
        This function will move the cursor to the beginning of the line editor
        at the end.

        Before::

            (Query): user query here|
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here

        Before::

            |   # <- this line is empty
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here
        """
        self.move_to_start()
        self.print_str(self.terminal.clear_eol(), end="")

    def update_line_editor(
        self,
        line_editor: LineEditor,
    ) -> str:  # pragma: no cover
        """
        Replace the user input with the new line editor, and move the cursor
        to the beginning of the next line, so it's ready to print the
        dropdown menu.

        :param line_editor: the new :class:`~zelfred.line_editor.LineEditor` object.

        :return: text of the line editor.
        """
        self.clear_line_editor()
        return self.print_line_editor(line_editor)

    # --------------------------------------------------------------------------
    # dropdown
    # --------------------------------------------------------------------------
    def process_title(
        self,
        title: str,
        line_width: int,
    ):  # pragma: no cover
        """
        Make sure the title fix the width of the terminal UI.

        :param title: the item title.
        :param line_width: the max width of the terminal UI, it will truncate
            the title and subtitle if they are too long.
        """
        space = line_width - 4 - 1
        if len(title) > space:
            half = (space - 3) // 2
            return title[:half] + "..." + title[-half:]
        else:
            return title

    def process_subtitle(
        self,
        subtitle: str,
        line_width: int,
    ):  # pragma: no cover
        """
        Make sure the subtitle fix the width of the terminal UI.

        :param subtitle: the item subtitle.
        :param line_width: the max width of the terminal UI, it will truncate
            the title and subtitle if they are too long.
        """
        space = line_width - 6 - 1
        if len(subtitle) > space:
            half = (space - 3) // 2
            return subtitle[:half] + "..." + subtitle[-half:]
        else:
            return subtitle

    def print_item(
        self,
        item: T_ITEM,
        selected: bool,
        line_width: int,
    ):  # pragma: no cover
        """
        Render one item in the dropdown menu. It looks like::

            [x] item 1 title here
                - item 1 subtitle here

        :param item: the :class:`~zelfred.item.Item` object to render.
        :param line_width: the max width of the terminal UI, it will truncate
            the title and subtitle if they are too long.
        """
        if selected:
            color = self.terminal.cyan
            symbol = self.checked_mark
        else:
            color = self.terminal.normal
            symbol = self.not_checked_mark

        self.print_line(
            "{t.bold}{color}{symbol} {color}{title}{t.normal}",
            color=color,
            symbol=symbol,
            title=self.process_title(item.title_text, line_width),
            t=self.terminal,
        )
        self.print_line(
            "{pad}{t.normal}{subtitle}",
            pad=self.subtitle_pad,
            subtitle=self.process_subtitle(item.subtitle_text, line_width),
            t=self.terminal,
        )

    def print_dropdown(
        self,
        dropdown: Dropdown,
        line_width: int,
    ) -> int:  # pragma: no cover
        """
        Render all items in the dropdown menu, it looks like::

            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here

        It assumes that the terminal UI is showing the query line editor and
        there's no item in the dropdown menu in the terminal UI before running this.

        :param dropdown: the :class:`~zelfred.dropdown.Dropdown` object to render.
        :param line_width: the max width of the terminal UI, it will truncate
            the title and subtitle if they are too long.

        :return: number of items rendered.
        """
        # the current terminal height may not be able to fit all items,
        # so we may need to update the ``self.dropdown._show_items_limit``
        # to fit the terminal height.
        terminal_height = self.terminal.height
        if terminal_height <= 9:
            raise TerminalTooSmallError(
                "Terminal height is too small to render the UI! "
                "It has to have at least 8 lines."
            )
        terminal_items_limit = (terminal_height - 3) // 2
        dropdown.show_items_limit = min(
            dropdown.show_items_limit,
            terminal_items_limit,
        )

        # raise error if the terminal width is too small
        terminal_width = self.terminal.width
        final_line_width = min(terminal_width, line_width)
        if terminal_width < 80:
            raise TerminalTooSmallError(
                "Terminal width is too small to render the UI! "
                "It has to have at least 80 ascii character wide."
            )

        # if the cursor is at the first line, move to beginning of the second line
        # before printing
        if self.line_number == 0:
            print(self.terminal.move_down, end="")
            print("\r", end="")
            sys.stdout.flush()

        # print the dropdown menu
        menu = dropdown.menu
        for item, selected in dropdown.menu:
            self.print_item(item, selected=selected, line_width=final_line_width)
        n_item = len(menu)
        return n_item

    def clear_dropdown(self):  # pragma: no cover
        """
        Before::

            (Query): user query here|
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here

        Before::

            (Query): user query here
            |
        """
        self.move_to_end()
        # self._debug()
        if self.n_lines > 1:
            self.clear_n_lines(n=self.line_number - 1)

    def update_dropdown(
        self,
        dropdown: Dropdown,
        line_width: int,
    ) -> int:  # pragma: no cover
        """
        Replace the user input with the new line editor, and move the cursor
        to the beginning of the next line, so it's ready to print the
        dropdown menu.

        :param dropdown: the :class:`~zelfred.dropdown.Dropdown` object to render.
        :param line_width: the max width of the terminal UI, it will truncate
            the title and subtitle if they are too long.

        :return: number of items rendered.
        """
        self.clear_dropdown()
        return self.print_dropdown(dropdown, line_width)

    def move_cursor_to_line_editor(
        self,
        line_editor: LineEditor,
    ) -> T.Tuple[int, int]:  # pragma: no cover
        """
        After the :meth:`Dropdown.print_dropdown` is called, the cursor is at the
        end of the UI. This method moves the cursor back to the user input box,
        so user can keep typing.

        Here's an example::

            (Query): user query here| <- want to move to here
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here
            | <- cursor is currently here

        :return: n_vertical is the number of line to move up, n_horizontal is
            the number of character to move right.
        """
        n_vertical = self.move_to_start()
        n_horizontal = len(self.prompt) + 2 + line_editor.cursor_position
        self.print_str(self.terminal.move_right(n_horizontal), end="")
        return n_vertical, n_horizontal

    def print_ui(
        self,
        line_editor: LineEditor,
        dropdown: Dropdown,
    ) -> int:  # pragma: no cover
        """
        Render the entire UI, and move the cursor to the right position.

        It assumes the terminal has nothing.
        """
        self.print_line_editor(line_editor)
        n_items = self.print_dropdown(dropdown, line_width=self.terminal.width)
        self.move_cursor_to_line_editor(line_editor)
        return n_items

    def move_to_end(self) -> int:  # pragma: no cover
        """
        Move the cursor to the end, this method will be used before exit.
        Here's an example::

            (Query): user query here| <- cursor is currently here
            [x] item 1 title here
                  item 1 subtitle here
            [ ] item 2 title here
                  item 2 subtitle here
            [ ] item 3 title here
                  item 3 subtitle here
            | <- want to move to here

        :param n_items: number of items in the dropdown menu.
        """
        if self.n_lines == 1 and self.line_number == 0:
            move_down_n_lines = 1
        else:
            move_down_n_lines = self.n_lines - self.line_number
        # print(f"n_lines = {self.n_lines}, line_number = {self.line_number}, move_down_n_lines = {move_down_n_lines}") # DEBUG ONLY
        if move_down_n_lines:
            self.print_str(move_down_n_lines * self.terminal.move_down, end="")
            self.line_number += move_down_n_lines
        return move_down_n_lines

    def clear_ui(self):  # pragma: no cover
        """
        Clear the entire UI, and move the cursor to the right position.
        """
        self.clear_dropdown()
        self.clear_line_editor()
