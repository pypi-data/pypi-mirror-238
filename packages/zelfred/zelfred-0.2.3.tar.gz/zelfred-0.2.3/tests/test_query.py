# -*- coding: utf-8 -*-

from zelfred.query import Query, QueryParser


class TestQueryParser:
    def test_parse(self):
        qp = QueryParser(delimiter="/")
        q = qp.parse(" bucket / artifacts / / deploy.zip")
        assert q.parts == [" bucket ", " artifacts ", " ", " deploy.zip"]
        assert q.trimmed_parts == ["bucket", "artifacts", "deploy.zip"]

        qp = QueryParser(delimiter=[" ", "-", "_"])
        q = qp.parse(" a b-c d_e f-g_h ")
        assert q.trimmed_parts == list("abcdefgh")


class TestQuery:
    def test_from_str(self):
        q = Query.from_str("  a   b   c  ")
        assert q.trimmed_parts == list("abc")


if __name__ == "__main__":
    from zelfred.tests import run_cov_test

    run_cov_test(__file__, "zelfred.query", preview=False)
