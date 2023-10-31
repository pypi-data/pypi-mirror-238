# -*- coding: utf-8 -*-

from zelfred.item import T_ITEM, Item, DEFAULT_TITLE, DEFAULT_SUBTITLE


class TestItem:
    def test(self):
        # test title and subtitle
        item = Item(title="hello")
        assert item.title_text == "hello"
        assert item.subtitle_text == DEFAULT_SUBTITLE

        item = Item(title="", subtitle="world")
        assert item.title_text == DEFAULT_TITLE
        assert item.subtitle_text == "world"

        # default handler should have no effect.
        item.enter_handler(ui=None)
        item.ctrl_a_handler(ui=None)
        item.ctrl_w_handler(ui=None)
        item.ctrl_p_handler(ui=None)

        # default uid should be an uuid
        item = Item(title="hello")
        assert len(item.uid) == 32

        item1 = Item(title="hello")
        item2 = Item(title="hello")
        assert item1.uid != item2.uid


if __name__ == "__main__":
    from zelfred.tests import run_cov_test

    run_cov_test(__file__, "zelfred.item", preview=False)
