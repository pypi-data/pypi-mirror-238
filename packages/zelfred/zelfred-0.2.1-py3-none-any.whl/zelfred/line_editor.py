# -*- coding: utf-8 -*-

"""
Line editor implementation.
"""

SEP_LIST = "!@#$%^&*()-+={[}]|\\:;" "<,>.?/"


def _normalize_separator(s: str, seps: str = SEP_LIST) -> str:
    for sep in seps:
        s = s.replace(sep, " ")
    return s


class LineEditor:
    """
    Simulate a user input line editor. User can type characters, move cursor,
    backspace, delete, clear line, etc ...

    For example, the ``(Query): beautiful|`` (``|`` is the cursor) in the
    following UI is the line editor.

    .. code-block:: bash

        (Query): beautiful|
        [x] Beautiful is better than ugly.
              subtitle 01
        [ ] Explicit is better than implicit.
              subtitle 02
        [ ] Simple is better than complex.
              subtitle 03

    Empty line editor:

    .. code-block:: bash

        |

    User entered some text, and the cursor is at the end:

    .. code-block:: bash

        my text|

    User entered some text, and the cursor is in the middle:

    .. code-block:: bash

        my |text

    :param chars: a list of characters, representing the current line.
        For example, if ``chars = ["m", "y", " ", "t", "e", "x", "t"]``,
        then the current line is ``my text``.
    :param cursor_position: the current cursor position. 0 means the cursor is
        at the beginning of the line. 1 means it is after the first character.
        when cursor_position == len(chars), it means the cursor is at the end.
        For example, if the text is ``my text`` and the ``cursor_position = 5``
        Then the cursor is at ``my te|xt``.
    """

    def __init__(self):
        self.chars = []
        self.cursor_position = 0

    def is_cursor_at_begin_of_line(self) -> bool:
        """
        Check if the cursor is at the beginning of the line.
        """
        return self.cursor_position == 0

    def is_cursor_at_end_of_line(self) -> bool:
        """
        Check if the cursor is at the end of the line.
        """
        return self.cursor_position == len(self.chars)

    def enter_text(self, text: str):
        """
        Enter text into the line editor.
        """
        for char in text:
            self.press_key(key=char)

    def _press_key(self, key: str):
        if self.is_cursor_at_end_of_line():
            self.chars.append(key)
            self.cursor_position += 1
        else:
            self.chars.insert(self.cursor_position, key)
            self.cursor_position += 1

    def press_key(self, key: str, n: int = 1):
        """
        Enter a key into the line editor. Also move cursor to the right.

        :param key: the entered character of the key.
        :param n: number of times to enter the key.
        """
        for _ in range(n):
            self._press_key(key)

    def _press_backspace(self):
        if self.cursor_position == 0:
            pass
        elif self.cursor_position == len(self.chars):
            self.chars.pop()
            self.cursor_position -= 1
        else:
            self.cursor_position -= 1
            self.chars.pop(self.cursor_position)

    def press_backspace(self, n: int = 1):
        """
        Delete character backwards in the line editor. Also move cursor to the left.

        :param n: number of characters to delete.
        """
        for _ in range(n):
            self._press_backspace()

    def _press_left(self):
        if self.cursor_position != 0:
            self.cursor_position -= 1

    def press_left(self, n: int = 1):
        """
        Move cursor to the left.

        :param n: number of times to move cursor to the left.
        """
        for _ in range(n):
            self._press_left()

    def press_home(self):
        """
        Move cursor to the beginning of the line.
        """
        self.cursor_position = 0

    def _press_delete(self):
        if self.cursor_position == len(self.chars):
            pass
        else:
            self.chars.pop(self.cursor_position)

    def press_delete(self, n: int = 1):
        """
        Delete character forwards in the line editor. Also, the cursor stays.

        :param n: number of characters to delete.
        """
        for _ in range(n):
            self._press_delete()

    def _press_right(self):
        if self.cursor_position != len(self.chars):
            self.cursor_position += 1

    def press_right(self, n: int = 1):
        """
        Move cursor to the right.

        :param n: number of times to move cursor to the right.
        """
        for _ in range(n):
            self._press_right()

    def press_end(self):
        """
        Move cursor to the end of the line.
        """
        self.cursor_position = len(self.chars)

    def clear_line(self):
        """
        Delete all user inputs and move cursor to the beginning of the line.
        """
        self.chars.clear()
        self.cursor_position = 0

    def clear_backward(self):
        """
        Delete all user inputs before the cursor and move cursor to the
        beginning of the line.
        """
        self.chars = self.chars[self.cursor_position :]
        self.cursor_position = 0

    def clear_forward(self):
        """
        Delete all user inputs after the cursor and the cursor stays.
        """
        self.chars = self.chars[: self.cursor_position]
        self.cursor_position = len(self.chars)

    def replace_text(self, text: str):
        """
        Replace all user inputs with the given text.

        :param text: the text to replace with.
        """
        self.clear_line()
        self.enter_text(text)

    move_to_start = press_home
    move_to_end = press_end

    def _locate_previous_word_position(self) -> int:
        """
        Locate the cursor position of the beginning of previous word.
        """
        # 先获得光标之前的字符串
        line = self.value
        # 按照空格分割开, words 里面的元素可以是空字符串
        words = _normalize_separator(line).split(" ")
        # print(f"before: words = {words}")
        # 从后往前找到第一个非空字符串的 index
        ind = None
        for i, word in enumerate(words[::-1]):
            if word:
                ind = i
                break
        # print(f"ind = {ind}")
        # 如果找到了非空字符串
        if ind is not None:
            # 那么保留所有非空字符串之前的 word, 并把最后一个非空字符串替换成空字符串
            # 这样即可算的 cursor position
            if ind:
                words = words[:-ind]
            words[-1] = ""
            # print(f"after: words = {words}")
            return len(" ".join(words))
        # 如果找不到非空字符串, 则移动到行首
        else:
            return 0

    def move_word_backward(self):
        """
        Move cursor to the beginning of previous word.
        """
        self.cursor_position = self._locate_previous_word_position()

    def delete_word_backward(self):
        """
        Delete the previous word.
        """
        delta = self.cursor_position - self._locate_previous_word_position()
        self.press_backspace(delta)

    def _locate_next_word_position(self) -> int:
        """
        Locate the cursor position of the beginning of next word.
        """
        # 先获得光标之后的字符串
        line = "".join(self.chars[self.cursor_position :])
        # 按照空格分割开, words 里面的元素可以是空字符串
        words = _normalize_separator(line).split(" ")
        # print(f"before: words = {words}")
        # 从前往后找到第一个非空字符串
        ind = None
        for i, word in enumerate(words):
            if word:
                ind = i
                break
        # print(f"ind = {ind}")
        # 如果找到了非空字符串, 则计算这个非空字符串起之前的所有字符串的总长度
        # 这个长度就是 cursor 要移动的距离
        if ind is not None:
            words = words[: (ind + 1)]
            # print(f"after: words = {words}")
            return self.cursor_position + len(" ".join(words))
        # 如果找不到非空字符串, 则移动到行尾
        else:
            return len(self.chars)

    def move_word_forward(self):
        """
        Move cursor to the beginning of next word.
        """
        self.cursor_position = self._locate_next_word_position()

    def delete_word_forward(self):
        """
        Delete the next word.
        """
        delta = self._locate_next_word_position() - self.cursor_position
        self.press_delete(delta)

    @property
    def line(self) -> str:
        """
        Return the displayed line.

        Example: ``ali|ce`` -> line = alice
        """
        return "".join(self.chars)

    @property
    def value(self) -> str:
        """
        The value of the user input, it is the text before the cursor.

        Example: ``ali|ce`` -> value = ali
        """
        return "".join(self.chars[: self.cursor_position])
