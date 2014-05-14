import js2xml
import js2xml.jsonlike
from nose.tools import *


def test_json():
    jscode_snippets = [
        (
            r"""
            var arr1 = ["a","b","c"];
            var arr2 = ["d","e","f"];
            """,
            [['a', 'b', 'c'],
             ['d', 'e', 'f']]
        ),
        (
            r"""
            var arr1 = ["a", null, "c"];
            var arr2 = [null, "e", null];
            """,
            [['a', None, 'c'],
             [None, 'e', None]]
        ),
        (
            r"""
            var arr1 = ["a", undefined, "c"];
            var arr2 = [undefined, "e", null];
            """,
            [['a', 'undefined', 'c'],
             ['undefined', 'e', None]]
        ),
        (
            r"""
            var i = -3.14;
            """, []
            ),
        (
            r"""
            money = {
                'quarters': 20
            };
            """,
            [{"quarters": 20}]
        ),
        (
            r"""
            money = {
                'quarters': 10,
                'addQuarters': function(amount) {
                    this.quarters += amount;
                }
            };
            money.addQuarters(10);
            """,
            []
        ),
        (
            r"""
            var money = {
                'quarters': 10,
                'something': [1,2,3,4],
                'somethingelse': {'nested': [5,6,7,8]},
                'addQuarters': function(amount) {
                    this.quarters += amount;
                }
            };
            money.addQuarters(10);
            """,
            [[1,2,3,4], {'nested': [5,6,7,8]}]
        ),
        (
            r"""
            var store = {
                'apples': 10,
                'carrots': [1,2,3,4],
                'chicken': {'eggs': [5,6,7,8]}
            };
            """,
            [{'apples': 10,
              'carrots': [1, 2, 3, 4],
              'chicken': {'eggs': [5, 6, 7, 8]}}]
        ),
        (
            r"""
            var store1 = {
                'apples': 10,
                'carrots': [1,2,3,4],
                'chicken': {'eggs': [5,6,7,8]}
            };
            var store2 = {
                'tomatoes': 20,
                'potatoes': [9, false, 7, 6],
                'spinach': {'cans': [true, 2]}
            };
            """,
            [{'apples': 10,
              'carrots': [1, 2, 3, 4],
              'chicken': {'eggs': [5, 6, 7, 8]}},
             {'potatoes': [9, False, 7, 6],
              'spinach': {'cans': [True, 2]},
              'tomatoes': 20}]
        ),
    ]

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        results = js2xml.jsonlike.findall(jsxml)
        assert_list_equal([js2xml.jsonlike.make_dict(r) for r in results], expected)

    for snippet, expected in jscode_snippets:
        jsxml = js2xml.parse(snippet)
        assert_list_equal(js2xml.jsonlike.getall(jsxml), expected)
