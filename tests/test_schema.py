import lxml.etree
import js2xml
from nose.tools import *


def test_schema():
    jscode_snippets = [

        # strings
        (
        r"""
        "test";
        """,
        """
<program>
  <string>test</string>
</program>

        """
        ),
        (
        r"""
        "test\
        multiline";
        """,
        """
<program>
  <string>test        multiline</string>
</program>
        """
        ),

        # numbers
        (
        "3.14;",
        """
<program>
  <number value="3.14"/>
</program>
        """
        ),
        (
        "-12;",
        """
<program>
  <number value="-12"/>
</program>
        """
        ),
        (
        "3.45e2;",
        """
<program>
  <number value="3.45e2"/>
</program>
        """
        ),
        (
        "0377;",
        """
<program>
  <number value="0377"/>
</program>
        """
        ),
        (
        "0xFF;",
        """
<program>
  <number value="0xFF"/>
</program>
        """
        ),

        # arrays
        (
        "[]",
"""
<program>
  <array/>
</program>
"""
        ),
        (
        "[1,2]",
        """
<program>
  <array>
    <number value="1"/>
    <number value="2"/>
  </array>
</program>
        """
        ),
        (
        "[1,,2]",
        """
<program>
  <array>
    <number value="1"/>
    <undefined/>
    <number value="2"/>
  </array>
</program>
        """
        ),
        (
        "[1,,2,,,3,]",
        """
<program>
  <array>
    <number value="1"/>
    <undefined/>
    <number value="2"/>
    <undefined/>
    <undefined/>
    <number value="3"/>
  </array>
</program>
        """
        ),
        (
        "['a', 'b','c']",
        """
<program>
  <array>
    <string>a</string>
    <string>b</string>
    <string>c</string>
  </array>
</program>

        """
        ),
        (
        "[a, 'b', c]",
        """
<program>
  <array>
    <identifier name="a"/>
    <string>b</string>
    <identifier name="c"/>
  </array>
</program>

        """
        ),

        # objects
        (
        "o = {};",
"""
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object/>
    </right>
  </assign>
</program>
"""
        ),
        (
        "o = {a: 1};",
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object>
        <property name="a">
          <number value="1"/>
        </property>
      </object>
    </right>
  </assign>
</program>

        """
        ),
        (
        "o = {a: 1, b: 2};",
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object>
        <property name="a">
          <number value="1"/>
        </property>
        <property name="b">
          <number value="2"/>
        </property>
      </object>
    </right>
  </assign>
</program>
        """
        ),
        (
        "o = {'c': 1, 'd': 2};",
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object>
        <property name="c">
          <number value="1"/>
        </property>
        <property name="d">
          <number value="2"/>
        </property>
      </object>
    </right>
  </assign>
</program>

        """
        ),
        (
        'o = {"c": 1, "d": 2};',
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object>
        <property name="c">
          <number value="1"/>
        </property>
        <property name="d">
          <number value="2"/>
        </property>
      </object>
    </right>
  </assign>
</program>

        """
        ),
        (
        'o = {"c": 1, d: "e"};',
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="o"/>
    </left>
    <right>
      <object>
        <property name="c">
          <number value="1"/>
        </property>
        <property name="d">
          <string>e</string>
        </property>
      </object>
    </right>
  </assign>
</program>

        """
        ),
        (
        "e = {foo: 5, bar: 6, baz: ['Baz', 'Content']};",
        """
<program>
  <assign operator="=">
    <left>
      <identifier name="e"/>
    </left>
    <right>
      <object>
        <property name="foo">
          <number value="5"/>
        </property>
        <property name="bar">
          <number value="6"/>
        </property>
        <property name="baz">
          <array>
            <string>Baz</string>
            <string>Content</string>
          </array>
        </property>
      </object>
    </right>
  </assign>
</program>

        """
        ),
        # other primitive data types
        (
        "null;",
        """
<program>
  <null/>
</program>

        """
        ),
        (
        "undefined;",
        """
<program>
  <undefined/>
</program>

        """
        ),
        (
        "true;",
        """
<program>
  <boolean>true</boolean>
</program>

        """
        ),
        (
        "false;",
        """
<program>
  <boolean>false</boolean>
</program>

        """
        ),

        # variables
        (
        r"""
        var i;
        """,
        """
<program>
  <var name="i"/>
</program>

        """
        ),
        (
        r"""
        var i,j,k;
        """,
        """
<program>
  <var name="i"/>
  <var name="j"/>
  <var name="k"/>
</program>

        """
        ),
        (
        r"""
        var i = 0;
        """,
        """
<program>
  <var name="i">
    <number value="0"/>
  </var>
</program>

        """
        ),
        (
        r"""
        var i = "test";
        """,
        """
<program>
  <var name="i">
    <string>test</string>
  </var>
</program>

        """
        ),
        (
        r"""var z = 'foxes', r = 'birds';""",
        """
<program>
  <var name="z">
    <string>foxes</string>
  </var>
  <var name="r">
    <string>birds</string>
  </var>
</program>

        """
        ),
        (
        r"""
        var i, j, k = 0;
        """,
        """
<program>
  <var name="i"/>
  <var name="j"/>
  <var name="k">
    <number value="0"/>
  </var>
</program>

        """
        ),
        (
        r"""
        var i=1, j, k = 2;
        """,
        """
<program>
  <var name="i">
    <number value="1"/>
  </var>
  <var name="j"/>
  <var name="k">
    <number value="2"/>
  </var>
</program>
        """
        ),
        (
        r"""
        var i = obj.prop;
        """,
        ""
        ),
        (
        r"""var testObj = {};""",
        ""
        ),
        (
        r"""var testObj = [];""",
        ""
        ),

        # assignements
        (
        r"""
        i = b;
        """,
        ""
        ),
        (
        r"""
        i.a = "b";
        """,
        ""
        ),
        (
        r"""
        i["a"] = "b";
        """,
        ""
        ),
        (
        r"""
        i[a] = "b";
        """,
        ""
        ),

        # control structures
        (
        r"""
        if (condition) {
            result = expression;
        };""",
        ""
        ),
        (
        r"""
        if (condition) {
            result = expression;
        } else {
            result = alternative;
        };""",
        ""
        ),

        (
        r"""
        if (exprA == exprB) {
           result = expression;
        } else if (expr2) {
           result = alternative1;
        } else {
           result = alternative2;
        };""",
        ""
        ),

        (
        "result = condition ? expression : alternative;",
        ""
        ),

        # switch
        (
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
        """,
        ""
        ),

        # for loop
        (
        r"""
        for (var i = 0; i < 5; i++) {
            a = i;
        }
        """,
        ""
        ),
        (
        r"""
        for (var i = 0; i < 5; i++) {
            a = i
        }
        """,
        ""
        ),
        (
        r"""
        for (var key in array) {
            continue;
        }
        """,
        ""
        ),
        (
        r"""
        for (;;) {
            break;
        }
        """,
        ""
        ),
        (
        r"""
        for (; i < len; i++) {
            text += cars[i] + "<br>";
        }
        """,
        ""
        ),
        (
        r"""
        for (var i = 0, len = cars.length, text = ""; i < len; i++) {
            text += cars[i] + "<br>";
        }
        """,
        ""
        ),
        (
        """
        for (; i < len; ) {
            text += cars[i] + "<br>";
            i++;
        }
        """,
        ""
        ),

        # while loop
        (
        """
        while (a<b) {
           a+=1;
        }
        """,
        ""
        ),
        (
        """
        do {
           a+=1;
         } while (a<b);
        """,
        ""
        ),

        # with
        (
        """
        with (document) {
           var a = getElementById('a');
           var b = getElementById('b');
           var c = getElementById('c');
         };
        """,
        ""
        ),

        # label
        (
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
        ""
        ),

        # functions
        (
        """
        function foo(p) {
            p = "bar";
        }
        """,
        ""
        ),
        (
        """
        function hello() {
            alert('world');
        }
        """,
        ""
        ),
        (
        """
        var anon = function() {
            alert('I am anonymous');
        };
        """,
        ""
        ),
        (
        """
        anon();
        """,
        ""
        ),
        (
        """
        setTimeout(function() {
            alert('hello');
        }, 1000)
        """,
        ""
        ),
        (
        """
        (function() {
            alert('foo');
        }());
        """,
        ""
        ),

        # get/set
        (
        """
        var obj = {
          get latest () {
            return "latest";
          }
        }
        """,
        ""
        ),
        (
        """
        delete obj.latest;
        """,
        ""
        ),
        (
        """
        var o = {
          set current (str) {
            return this.log[this.log.length] = str;
          },
          log: []
        }
        """,
        ""
        ),

    ]

    for snippet, expected in jscode_snippets:
        print snippet
        js = js2xml.parse(snippet)
        output = js2xml.pretty_print(js).strip()
        assert_equal(output, expected.strip(), "got\n%s\nexpected:\n%s" % (output, expected))
