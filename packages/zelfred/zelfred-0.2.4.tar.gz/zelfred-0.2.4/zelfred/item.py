# -*- coding: utf-8 -*-

"""
Item is the basic building block of the terminal UI. It represents a single
selectable item in the dropdown menu. User can move or scroll selector up and down
to select an item, and then perform :mod:`~zelfred.action`.
"""

import typing as T
import uuid
import dataclasses

from .constants import DEFAULT_TITLE, DEFAULT_SUBTITLE
from .exc import EndOfInputError


if T.TYPE_CHECKING:  # pragma: no cover
    from .ui import UI


def gen_uid() -> str:
    return uuid.uuid4().hex


@dataclasses.dataclass
class Item:
    """
    Represent an item in the terminal UI. In the example below, the
    ``[x] Beautiful is better than ugly`` and ``subtitle 01`` is one item.

    .. code-block:: bash

        (Query):
        [x] Beautiful is better than ugly.
              subtitle 01
        [ ] Explicit is better than implicit.
              subtitle 02
        [ ] Simple is better than complex.
              subtitle 03

    :param uid: item unique id. The UI use this to distinguish different items.
    :param title: first line of the item. It has a checkbox in front of it to
        indicate whether it is selected.
    :param subtitle: second line of the item.
    :param arg: argument that will be passed to the action.
    :param autocomplete: the text that will be filled in the input box when
        user hits ``TAB`` key.
    :param variables: arbitrary dictionary object, it can be used in the action.
    """

    title: str = dataclasses.field()
    subtitle: T.Optional[str] = dataclasses.field(default=None)
    uid: str = dataclasses.field(default_factory=gen_uid)
    arg: T.Optional[str] = dataclasses.field(default=None)
    autocomplete: T.Optional[str] = dataclasses.field(default=None)
    variables: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)

    @property
    def title_text(self) -> str:
        return self.title or DEFAULT_TITLE

    @property
    def subtitle_text(self) -> str:
        return self.subtitle or DEFAULT_SUBTITLE

    def enter_handler(self, ui: "UI"):
        """
        This is the abstract method that will perform user defined action
        when user hits ``Enter`` on this item. Develop should inherit this class
        and override this method to perform user defined action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        pass

    def post_enter_handler(self, ui: "UI"):  # pragma: no cover
        """
        This is the abstract method that will update the UI after taking user action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        # ui.render.clear_n_lines(1)
        ui.need_run_handler = False
        raise EndOfInputError(selection=self)

    def ctrl_a_handler(self, ui: "UI"):
        """
        This is the abstract method that will perform user defined action
        when user hits ``Ctrl + A`` on this item. Develop should inherit this class
        and override this method to perform user defined action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        pass

    def post_ctrl_a_handler(self, ui: "UI"):  # pragma: no cover
        """
        This is the abstract method that will update the UI after taking user action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        ui.need_run_handler = False
        raise EndOfInputError(selection=self)

    def ctrl_w_handler(self, ui: "UI"):
        """
        This is the abstract method that will perform user defined action
        when user hits ``Ctrl + W`` on this item. Develop should inherit this class
        and override this method to perform user defined action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        pass

    def post_ctrl_w_handler(self, ui: "UI"):  # pragma: no cover
        """
        This is the abstract method that will update the UI after taking user action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        ui.need_run_handler = False
        raise EndOfInputError(selection=self)

    def ctrl_u_handler(self, ui: "UI"):
        """
        This is the abstract method that will perform user defined action
        when user hits ``Ctrl + U`` on this item. Develop should inherit this class
        and override this method to perform user defined action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        pass

    def post_ctrl_u_handler(self, ui: "UI"):  # pragma: no cover
        """
        This is the abstract method that will update the UI after taking user action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        ui.need_run_handler = False
        raise EndOfInputError(selection=self)

    def ctrl_p_handler(self, ui: "UI"):
        """
        This is the abstract method that will perform user defined action
        when user hits ``Ctrl + P`` on this item. Develop should inherit this class
        and override this method to perform user defined action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        pass

    def post_ctrl_p_handler(self, ui: "UI"):  # pragma: no cover
        """
        This is the abstract method that will update the UI after taking user action.

        :param ui: the :class:`~zelfred.ui.UI` object.
        """
        ui.need_run_handler = False
        raise EndOfInputError(selection=self)


T_ITEM = T.TypeVar("T_ITEM", bound=Item)
