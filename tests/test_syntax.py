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
        "e = {foo: 5, bar: 6, baz: ['Baz', 'Content']};",
        "e = {1: a, 2: b};",
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
        r"""
        if (exprA == exprB) {
           result = expression;
        } else if (expr2) {
           result = alternative1;
        } else {
           result = alternative2;
        };""",
        "result = condition ? expression : alternative;",
        # switch
        r"""
        switch (expr) {
           case SOMEVALUE:
             //statements;
             break;
           case ANOTHERVALUE:
             //statements;
             break;
           default:
             //statements;
             break;
         }
        """
        # for loop
        r"""
        for (var i = 0; i < 5; i++) {
            a = i;
        }
        """,
        r"""
        for (var i = 0; i < 5; i++) {
            a = i
        }
        """,
        r"""
        for (var key in array) {
            continue;
        }
        """,
        r"""
        for (;;) {
            break;
        }
        """,
        r"""
        for (; i < len; i++) {
            text += cars[i] + "<br>";
        }
        """,
        r"""
        for (var i = 0, len = cars.length, text = ""; i < len; i++) {
            text += cars[i] + "<br>";
        }
        """,
        """
        for (; i < len; ) {
            text += cars[i] + "<br>";
            i++;
        }
        """,
        # while loop
        """
        while (a<b) {
           a+=1;
        }
        """,
        """
        do {
           a+=1;
         } while (a<b);
        """,
        # with
        """
        with (document) {
           var a = getElementById('a');
           var b = getElementById('b');
           var c = getElementById('c');
         };
        """,
        # label
        r"""
        loop1: for (var a = 0; a < 10; a++) {
           if (a == 4) {
               break loop1; // Stops after the 4th attempt
           }
           alert('a = ' + a);
           loop2: for (var b = 0; b < 10; ++b) {
              if (b == 3) {
                 continue loop2; // Number 3 is skipped
              }
              if (b == 6) {
                 continue loop1; // Continues the first loop, 'finished' is not shown
              }
              alert('b = ' + b);
           }
           alert('finished')
        }
        block1: {
            alert('hello'); // Displays 'hello'
            break block1;
            alert('world'); // Will never get here
        }
        """,
        # functions
        """
        function foo(p) {
            p = "bar";
        }
        """,
        """
        function hello() {
            alert('world');
        }
        """,
        """
        var x = function(y) {
           return y * y;
        };
        """,
        """
        var math = {
          'factorial': function factorial(n) {
            if (n <= 1)
              return 1;
            return n * factorial(n - 1);
          }
        };
        """,
        """
        var anon = function() {
            alert('I am anonymous');
        };
        """,
        """
        anon();
        """,
        """
        setTimeout(function() {
            alert('hello');
        }, 1000)
        """,
        """
        (function() {
            alert('foo');
        }());
        """,
        # get/set
        """
        var obj = {
          get latest () {
            return "latest";
          }
        }
        """,
        """
        delete obj.latest;
        """,
        """
        var o = {
          set current (str) {
            return this.log[this.log.length] = str;
          },
          log: []
        }
        """,
        # new
        """var mycar = new car("Eagle", "Talon TSi", 1993);""",
        # try / catch
        """
        try {
           throw "myException"; // generates an exception
        }
        catch (e) {
           // statements to handle any exceptions
           logMyErrors(e); // pass exception object to error handler
        }
        """,
        """
        try {
            addalert("bad call");
        }
        catch(e) {
            document.write ("Error Message: " + e.message);
            document.write ("<br />");
            document.write ("Error Code: ");
            document.write (e.number & 0xFFFF);
            document.write ("<br />");
            document.write ("Error Name: " + e.name);
        }
        """,
        """
        try {
            document.write("Outer try running...<br/>");

            try {
                document.write("Nested try running...<br/>");
                throw new Error(301, "an error");
            }
            catch (e) {
                document.write ("Nested catch caught " + e.message + "<br/>");
                throw e;
            }
            finally {
                document.write ("Nested finally is running...<br/>");
            }
        }
        catch (e) {
            document.write ("Outer catch caught " + e.message + "<br/>");
        }
        finally {
            document.write ("Outer finally running");
        }
        """,
        """
        new Map
        """,
    ]

    for snippet in jscode_snippets:
        assert_is_not_none(js2xml.parse(snippet))
