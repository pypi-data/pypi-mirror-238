# -*- coding: utf-8 -*-

from zelfred.paths import dir_project_root
from zelfred.debug import Debugger


class TestDebugger:
    def test(self):
        debugger = Debugger()
        debugger.path_log_txt = dir_project_root / "tmp" / "log.txt"
        debugger.path_log_txt.parent.mkdir(parents=True, exist_ok=True)

        debugger.reset()
        debugger.enable()
        debugger.log("hello")
        assert debugger.path_log_txt.read_text().endswith("hello\n")

        debugger.disable()
        debugger.log("hello")
        assert debugger.path_log_txt.read_text().endswith("hello\n")

        debugger.enable()
        debugger.log("world")
        assert debugger.path_log_txt.read_text().endswith("world\n")


if __name__ == "__main__":
    from zelfred.tests import run_cov_test

    run_cov_test(__file__, "zelfred.debug", preview=False)
