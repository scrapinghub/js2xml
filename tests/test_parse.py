import js2xml
from nose.tools import *


def test_parse():
    jscode_snippets = [
        r"""
        var i = 0;
        """,
        r"""
        document.write("\n");
        """,
        r"""
        var t1 = "nested \"quote\".";
        var t2 = 'nested \'quote\'.';
        var t3 = 'nested \"quote\".';
        var t2 = "nested \'quote\'.";
        """
    ]

    for snippet in jscode_snippets:
        assert_is_not_none(js2xml.parse(snippet))


def test_parse_exception():
    jscode_snippets = [
        r"""
        var i = ';
        """,
        r"""
        {
            .document.write;
        }
        """,
        r"""
        var t = "nested "quote"."d;
        """,
        r"""
        t = -;
        """,
    ]

    for snippet in jscode_snippets:
        assert_raises(SyntaxError, js2xml.parse, snippet)
