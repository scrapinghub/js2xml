import js2xml
from nose.tools import *


def test_syntax():
    jscode_snippets = [

        # strings
        r"""
        "test";
        """,
        r"""
        "test\
        multiline";
        """,

        # numbers
        "3.14;",
        "-12;",
        "3.45e2;",
        "0377;",
        "0xFF;"

        # arrays
        "[]",
        "[1,2]",
        "[1,,2]",
        "[1,,2,,3,]",
        "['a', 'b','c']",
        "[a, 'b', c]",

        # objects
        "o = {};",
        "o = {a: 1};",
        "o = {a: 1, b: 2};",
        "o = {'c': 1, 'd': 2};",
        'o = {"c": 1, "d": 2};',
        'o = {"c": 1, d: "e"};',
        "e = {foo: 5, bar: 6, baz: ['Baz', 'Content']};"

        # other primitive data types
        "null;",
        "undefined;",
        "true;",
        "false;",

        # variables
        r"""
        var i;
        """,
        r"""
        var i,j,k;
        """,
        r"""
        var i = 0;
        """,
        r"""
        var i = "test";
        """,
        r"""var z = 'foxes', r = 'birds';""",
        r"""
        var i, j, k = 0;
        """,
        r"""
        var i=1, j, k = 2;
        """,
        r"""
        var i = obj.prop;
        """,
        r"""var testObj = {};""",
        r"""var testObj = [];""",

        # assignements
        r"""
        i = b;
        """,
        r"""
        i.a = "b";
        """,
        r"""
        i["a"] = "b";
        """,
        r"""
        i[a] = "b";
        """,

        # control structures
        r"""
        if (condition) {
            result = expression;
        };""",
        r"""
        if (condition) {
            result = expression;
        } else {
            result = alternative;
        };""",
    ]

    for snippet in jscode_snippets:
        assert_is_not_none(js2xml.parse(snippet))
