# -*- coding: utf-8 -*-

from zelfred import api


def test():
    _ = api
    _ = api.Item
    _ = api.T_ITEM
    _ = api.Query
    _ = api.QueryParser
    _ = api.UI
    _ = api.T_HANDLER
    _ = api.debugger
    _ = api.exc


if __name__ == "__main__":
    from zelfred.tests import run_cov_test

    run_cov_test(__file__, "afwf_shell.api", preview=False)
