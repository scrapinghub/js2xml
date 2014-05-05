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


def test_parse_string():
    jscode_snippets = [
        (
        r"""
        var i = 'test';
        """, [r'test']
        ),
        (
        r"""
        var i = 'test\'s output';
        """, [r"test's output"]
        ),
        (
        r"""
        var i = "test";
        """, [r'test']
        ),
        (
        r"""
        var i = "test\'s output";
        """, [r"test\'s output"]
        ),
        (
        r"""
        var i = "nested \"quotes\".";
        """, [r'nested "quotes".']
        ),
    ]

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        result = jsxml.xpath("//string/text()")
        assert_list_equal(result, expected)


def test_parse_url():
    jscode_snippets = [
        (
        r"""
        var i = 'http://www.example.com';
        """, [r'http://www.example.com']
        ),
        (
        r"""
        var i = 'http:\/\/www.example.com';
        """, [r"http://www.example.com"]
        ),
    ]

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        result = jsxml.xpath("//string/text()")
        assert_list_equal(result, expected)


def test_parse_number():
    jscode_snippets = [
        (
        r"""
        var i = 3;
        """, [r'3']
        ),
        (
        r"""
        var i = -3.14;
        """, [r"-3.14"]
        ),
    ]

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        result = jsxml.xpath("//number/text()")
        assert_list_equal(result, expected)
