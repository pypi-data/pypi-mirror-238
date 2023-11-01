# -*- coding: utf-8 -*-

"""
Dropdown menu implementation.
"""

import typing as T

from .constants import SHOW_ITEMS_LIMIT, SCROLL_SPEED
from .item import T_ITEM
from .exc import NoItemToSelectError


class Dropdown:
    """
    Simulate an items dropdown menu. User can move or scroll selector up and down
    to select an item, and then perform :mod:`~zelfred.action`.

    For example, the ``[x] Beautiful is better than ugly.``,
    ``[ ] Explicit is better than implicit.`` and
    the ``[ ] Simple is better than complex.`` part in the following UI is the
    dropdown menu.

    .. code-block:: bash

        (Query):
        [x] Beautiful is better than ugly.
              subtitle 01
        [ ] Explicit is better than implicit.
              subtitle 02
        [ ] Simple is better than complex.
              subtitle 03

    :param items: All items in this dropdown menu. We only show ``SHOW_ITEMS_LIMIT``
        items in the UI at a time
    :param n_items: total number of items, it is a cache of ``len(items)``.
    :param selected_item_index: the selected item index, the value can be larger
        than ``SHOW_ITEMS_LIMIT`` if we have many items.
    :param cursor_position: the selected item cursor position in the dropdown UI,
        it is a value from 0 to ``SHOW_ITEMS_LIMIT - 1``.
    :param show_items_limit:  max number of items to show in the UI.
    """

    def __init__(
        self,
        items: T.List[T_ITEM],
        show_items_limit: int = SHOW_ITEMS_LIMIT,
        scroll_speed: int = SCROLL_SPEED,
    ):
        self.items: T.List[T_ITEM] = items
        self.n_items: int = len(items)
        self.selected_item_index: int = 0
        self.cursor_position: int = 0
        self.show_items_limit = min(show_items_limit, self.n_items)
        self.scroll_speed = scroll_speed

    def update(self, items: T.List[T_ITEM]):
        """
        Update the dropdown menu with new items.
        """
        self.items = items
        self.n_items = len(items)
        self.selected_item_index = 0
        self.cursor_position = 0
        self.show_items_limit = min(SHOW_ITEMS_LIMIT, self.n_items)

    @property
    def selected_item(self) -> T_ITEM:
        """
        Return the selected item object. If there is no item, raise
        :class:`~zelfred.exc.NoItemToSelectError`.
        """
        try:
            return self.items[self.selected_item_index]
        except IndexError:
            raise NoItemToSelectError

    def _press_down(self) -> T.Tuple[int, int]:
        # already the last item
        if self.selected_item_index == self.n_items - 1:
            select_delta = 0
        else:
            self.selected_item_index += 1
            select_delta = 1
        # already the last item in the UI
        if self.cursor_position == self.show_items_limit - 1:
            cursor_delta = 0
        else:
            self.cursor_position += 1
            cursor_delta = 1
        return select_delta, cursor_delta

    def press_down(self, n: int = 1) -> T.Tuple[int, int]:
        """
        Move selector down to pick the next item (if possible) in the dropdown menu.

        Example, before ``dropdown.press_down()``:

        .. code-block:: bash

            (Query):
            [x] Beautiful is better than ugly.
                  subtitle 01
            [ ] Explicit is better than implicit.
                  subtitle 02
            [ ] Simple is better than complex.
                  subtitle 03

        After:

        .. code-block:: bash

            (Query):
            [ ] Beautiful is better than ugly.
                  subtitle 01
            [x] Explicit is better than implicit.
                  subtitle 02
            [ ] Simple is better than complex.
                  subtitle 03

        :param n: move selector down ``n`` times.

        :return: tuple of ``(select_delta, cursor_delta)``.
        """
        if n >= (self.n_items - 1 - self.selected_item_index):
            self.selected_item_index = self.n_items - 1
            self.cursor_position = self.show_items_limit - 1
            return 0, 0
        select_delta, cursor_delta = 0, 0
        for _ in range(n):
            select_delta_, cursor_delta_ = self._press_down()
            select_delta += select_delta_
            cursor_delta += cursor_delta_
        return select_delta, cursor_delta

    def _press_up(self) -> T.Tuple[int, int]:
        if self.selected_item_index == 0:
            select_delta = 0
        else:
            self.selected_item_index -= 1
            select_delta = -1
        if self.cursor_position == 0:
            cursor_delta = 0
        else:
            self.cursor_position -= 1
            cursor_delta = -1
        return select_delta, cursor_delta

    def press_up(self, n: int = 1) -> T.Tuple[int, int]:
        """
        Move selector up to pick the previous item (if possible) in the dropdown menu.

        Example, before ``dropdown.press_up()``:

        .. code-block:: bash

            (Query):
            [ ] Beautiful is better than ugly.
                  subtitle 01
            [ ] Explicit is better than implicit.
                  subtitle 02
            [x] Simple is better than complex.
                  subtitle 03

        After:

        .. code-block:: bash

            (Query):
            [ ] Beautiful is better than ugly.
                  subtitle 01
            [x] Explicit is better than implicit.
                  subtitle 02
            [ ] Simple is better than complex.
                  subtitle 03

        :param n: move selector up ``n`` times.

        :return: tuple of ``(select_delta, cursor_delta)``.
        """
        if n >= self.selected_item_index:
            self.selected_item_index = 0
            self.cursor_position = 0
            return 0, 0
        select_delta, cursor_delta = 0, 0
        for _ in range(n):
            select_delta_, cursor_delta_ = self._press_up()
            select_delta += select_delta_
            cursor_delta += cursor_delta_
        return select_delta, cursor_delta

    def scroll_down(self, n: int = 1) -> T.Tuple[int, int]:
        """
        Scroll the dropdown menu down to show more items, also move the selector.

        :param n: scroll down ``n`` times. Each time we scroll down ``SCROLL_SPEED`` items.

        :return: tuple of ``(select_delta, cursor_delta)``.
        """
        return self.press_down(n * self.scroll_speed)

    def scroll_up(self, n: int = 1) -> T.Tuple[int, int]:
        """
        Scroll the dropdown menu up to show more items, also move the selector.

        :param n: scroll up ``n`` times. Each time we scroll up ``SCROLL_SPEED`` items.

        :return: tuple of ``(select_delta, cursor_delta)``.
        """
        return self.press_up(n * self.scroll_speed)

    @property
    def menu(self) -> T.List[T.Tuple[T_ITEM, bool]]:
        """
        The list of items to show in the UI. The list is determined by
        ``selected_item_index`` ``cursor_position`` and ``show_items_limit``
        together. It is a subset of ``self.items``.

        :return: a list of tuples, each tuple contains an item and a boolean value
            indicating whether the item is selected or not.
        """
        # this code is for debug only
        # print(self.n_items)
        # print(self.selected_item_index)
        # print(self.cursor_position)

        lower_index = self.selected_item_index - self.cursor_position
        upper_index = self.selected_item_index + (
            self.show_items_limit - self.cursor_position
        )
        menu = list()
        for ind, item in enumerate(self.items[lower_index:upper_index]):
            if ind == self.cursor_position:
                menu.append((item, True))
            else:
                menu.append((item, False))
        return menu
