from js2xml import parse
from js2xml.utils.vars import get_vars


def test_vars():
    jscode_snippets = [
        (
            r"""
            var arr1 = ["a","b","c"];
            var arr2 = ["d","e","f"];
            """,
            {'arr1': ['a', 'b', 'c'],
             'arr2': ['d', 'e', 'f']}
        ),
        (
            r"""
            var arr1 = ["a", null, "c"];
            var arr2 = [null, "e", null];
            """,
            {'arr1': ['a', None, 'c'],
             'arr2': [None, 'e', None]}
        ),
        (
            r"""
            var arr1 = ["a", undefined, "c"];
            var arr2 = [undefined, "e", null];
            """,
            {'arr1': ['a', 'undefined', 'c'],
             'arr2': ['undefined', 'e', None]}
        ),
        (
            r"""
            var i = -3.14;
            """,
            {'i': -3.14}
        ),
        (
            r"""
            money = {
                'quarters': 20
            };
            """,
            {'money': {"quarters": 20}}
        ),
        (
            r"""
            money = {
                quarters: 20
            };
            """,
            {'money': {"quarters": 20}}
        ),
        (
            r"""
            currency = 'USD';
            money = {
                "value": 20,
                "currency": currency
            };
            """,
            {'currency': 'USD',
             'money': {'currency': 'currency', 'value': 20}}
        ),
        (
            r"""
            t = {a: "3", "b": 3, "3": 3.0};
            """,
            {'t': {'3': 3.0, 'a': '3', 'b': 3}}
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
            {'money': {'quarters': 10, 'addQuarters': None}}
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
            {'money': {'quarters': 10,
                       'addQuarters': None,
                       'something': [1,2,3,4],
                       'somethingelse': {'nested': [5,6,7,8]}}}
        ),
        (
            r"""
            var store = {
                'apples': 10,
                'carrots': [1,2,3,4],
                'chicken': {'eggs': [5,6,7,8]}
            };
            """,
            {'store':
                {'apples': 10,
                 'carrots': [1, 2, 3, 4],
                 'chicken': {'eggs': [5, 6, 7, 8]}}
            }
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
            {'store1': {
              'apples': 10,
              'carrots': [1, 2, 3, 4],
              'chicken': {'eggs': [5, 6, 7, 8]}},
             'store2':{
              'potatoes': [9, False, 7, 6],
              'spinach': {'cans': [True, 2]},
              'tomatoes': 20}
            }
        ),
    ]
    for snippet, expected in jscode_snippets:
        tree = parse(snippet)
        assert get_vars(tree) == expected, (snippet, expected)
