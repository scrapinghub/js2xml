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
        var h = 'test';
        var i = "test";
        var j = "";
        var k = '""';
        var l = '"';
        var m = '';
        var n = "''";
        var o = "'";
        """, ['test', 'test', '', '""', '"', '', "''", "'"]
        ),
        (
        r"""
        var i = 'test\'s output';
        """, [r"test's output"]
        ),
        (
        r"""
        var i = 'test\
 multiline';
        """, [r"test multiline"]
        ),
        (
        r"""
        var i = 'test\
 long \
 multiline';
        """, [r"test long  multiline"]
        ),

        (
        r"""
        var i = ["\"", '\''];
        var j = "test\'s output";
        var k = "test\\'s output";
        var l = "nested \"quotes\".";
        """, ['"', "'", r"test's output", r"test\'s output", r'nested "quotes".']
        ),
        (
        r"""
        var i = 'https://www.blogger.com/navbar.g?targetBlogID\0754325487278375417853\46blogName\75spirello\46publishMode\75PUBLISH_MODE_BLOGSPOT\46navbarType\75LIGHT\46layoutType\75LAYOUTS\46searchRoot\75http://spirelloskrimskramserier.blogspot.com/search\46blogLocale\75no\46v\0752\46homepageUrl\75http://spirelloskrimskramserier.blogspot.com/\46vt\0751357383140196484672';
        """, [r'https://www.blogger.com/navbar.g?targetBlogID=4325487278375417853&blogName=spirello&publishMode=PUBLISH_MODE_BLOGSPOT&navbarType=LIGHT&layoutType=LAYOUTS&searchRoot=http://spirelloskrimskramserier.blogspot.com/search&blogLocale=no&v=2&homepageUrl=http://spirelloskrimskramserier.blogspot.com/&vt=1357383140196484672']
        ),
        (
        r"""
        var i = "foo \
bar";
        var j = "foo \
                 bar";
        """, [r'foo bar', 'foo                  bar']
        ),
        (
        r"""
        var x = "\u00A9 Netscape Communications";
        """,
        [ur'\u00a9 Netscape Communications']
        ),
        (
        u"""
        var x = "\u00A9 Netscape Communications";
        """.encode("utf8"),
        [u'\u00a9 Netscape Communications']
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
        result = jsxml.xpath("//number/@value")
        assert_list_equal(result, expected)


def test_parse_undefined():
    jscode_snippets = [
        (
        r"""
        myArray = [0,1,,,4,5];
        """, 2
        ),
        (
        r"""
        myArray = [,1,,,4,];
        """, 3 # and not 4
        ),
        (r"""
        myArray = [,1,,,4,,,];
        """, 5
        ),
    ]

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        result = jsxml.xpath("count(//array/undefined)")
        assert_equal(result, expected)


def test_parse_encoding():

    jscode_snippets = [
        (u"""
        var test = "Daniel Gra\xf1a";
        """,
        None,
        [u"Daniel Gra\xf1a"]
        ),
        (u"""
        var test = "Daniel Gra\xf1a";
        """.encode("latin1"),
        "latin1",
        [u"Daniel Gra\xf1a"]
        ),
    ]

    for snippet, encoding, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet, encoding=encoding)
        result = jsxml.xpath("//string/text()")
        assert_equal(result, expected)
