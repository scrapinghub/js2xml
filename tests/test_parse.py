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
        # testing Unicode literals
        b"""
        var x = "\\u00A9 Netscape Communications 1";
        """,
        [u'\u00a9 Netscape Communications 1']
        ),
        (
        # testing Unicode characters
        u"""
        var x = "\u00A9 Netscape Communications 2";
        """.encode("utf8"),
        [u'\u00a9 Netscape Communications 2']
        ),
        # a real example
        (
        r"""
        var needleParam = needleParam || {};
        needleParam.chatGroup = "test";
        needleParam.productId = "6341292";
        needleParam.productPrice = "EUR              138.53".replace("$","n_").replace(/,/g,"");
        //Begin Needle (fan-sourcing platform) snippet
        jQuery(document).ready(function(){

        var e = document.createElement("script"); e.type = "text/javascript";
        e.async = true;
        e.src = document.location.protocol +

        "//overstock.needle.com/needle_service.js?1"; document.body.appendChild(e);

        });
        // End Needle snippet
        """,
        ['test',
         '6341292',
         'EUR              138.53',
         '$',
         'n_',
         '',
         'script',
         'text/javascript',
         '//overstock.needle.com/needle_service.js?1']
        ),
        # test replacing some control characters
        (
        r"""
        var name = "\u13e9\u0352\u0362\u044f\u2778\u00b3\u1d43\u034e\u034e\u0442\u035b\u13b7\u0362\u033b\u1d51A\u0362\u13de\u0001\u0001\u277c00b";
        """,
        [u'\u13e9\u0352\u0362\u044f\u2778\xb3\u1d43\u034e\u034e\u0442\u035b\u13b7\u0362\u033b\u1d51A\u0362\u13de\ufffd\ufffd\u277c00b']
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
