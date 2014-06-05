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
"""
<program>
  <var name="i">
    <dotaccessor>
      <object>
        <identifier name="obj"/>
      </object>
      <property>
        <identifier name="prop"/>
      </property>
    </dotaccessor>
  </var>
</program>
"""
        ),
        (
        r"""var testObj = {};""",
"""
<program>
  <var name="testObj">
    <object/>
  </var>
</program>
"""
        ),
        (
        r"""var testObj = [];""",
"""
<program>
  <var name="testObj">
    <array/>
  </var>
</program>
"""
        ),

        # operations
        (
        r"""
        1 + 2;
        "foo" + false;
        3 - 5
        """,
"""
<program>
  <binaryoperation operation="+">
    <left>
      <number value="1"/>
    </left>
    <right>
      <number value="2"/>
    </right>
  </binaryoperation>
  <binaryoperation operation="+">
    <left>
      <string>foo</string>
    </left>
    <right>
      <boolean>false</boolean>
    </right>
  </binaryoperation>
  <binaryoperation operation="-">
    <left>
      <number value="3"/>
    </left>
    <right>
      <number value="5"/>
    </right>
  </binaryoperation>
</program>
"""
        ),
        (
        r"""
        1.0 / 2.0;
        -2 * 2;
        12 % 5;
        """,
"""
<program>
  <binaryoperation operation="/">
    <left>
      <number value="1.0"/>
    </left>
    <right>
      <number value="2.0"/>
    </right>
  </binaryoperation>
  <binaryoperation operation="*">
    <left>
      <number value="-2"/>
    </left>
    <right>
      <number value="2"/>
    </right>
  </binaryoperation>
  <binaryoperation operation="%">
    <left>
      <number value="12"/>
    </left>
    <right>
      <number value="5"/>
    </right>
  </binaryoperation>
</program>
"""
        ),

        (
        r"""
        // Postfix
        var x = 3;
        y = x++; // y = 3, x = 4

        // Prefix
        var a = 2;
        b = ++a; // a = 3, b = 3
        """,
"""
<program>
  <var name="x">
    <number value="3"/>
  </var>
  <assign operator="=">
    <left>
      <identifier name="y"/>
    </left>
    <right>
      <postfix operation="++">
        <identifier name="x"/>
      </postfix>
    </right>
  </assign>
  <var name="a">
    <number value="2"/>
  </var>
  <assign operator="=">
    <left>
      <identifier name="b"/>
    </left>
    <right>
      <unaryoperation operation="++">
        <identifier name="a"/>
      </unaryoperation>
    </right>
  </assign>
</program>

"""     ),

        (
        r"""
        // Postfix
        var x = 3;
        y = x--; // y = 3, x = 2

        // Prefix
        var a = 2;
        b = --a; // a = 1, b = 1
        """,
"""
<program>
  <var name="x">
    <number value="3"/>
  </var>
  <assign operator="=">
    <left>
      <identifier name="y"/>
    </left>
    <right>
      <postfix operation="--">
        <identifier name="x"/>
      </postfix>
    </right>
  </assign>
  <var name="a">
    <number value="2"/>
  </var>
  <assign operator="=">
    <left>
      <identifier name="b"/>
    </left>
    <right>
      <unaryoperation operation="--">
        <identifier name="a"/>
      </unaryoperation>
    </right>
  </assign>
</program>
"""     ),

        (
        r"""
        var x = 3;
        y = -x; // y = -3, x = 3
        """,
"""
<program>
  <var name="x">
    <number value="3"/>
  </var>
  <assign operator="=">
    <left>
      <identifier name="y"/>
    </left>
    <right>
      <unaryoperation operation="-">
        <identifier name="x"/>
      </unaryoperation>
    </right>
  </assign>
</program>

"""
        ),

        (
        r"""
        +3;     // 3
        +"3";   // 3
        +true;  // 1
        +false; // 0
        +null;  // 0
        """,
"""
<program>
  <number value="+3"/>
  <unaryoperation operation="+">
    <string>3</string>
  </unaryoperation>
  <unaryoperation operation="+">
    <boolean>true</boolean>
  </unaryoperation>
  <unaryoperation operation="+">
    <boolean>false</boolean>
  </unaryoperation>
  <unaryoperation operation="+">
    <null/>
  </unaryoperation>
</program>
"""
        ),

        # assignements
        (
        r"""
        i = b;
        """,
"""
<program>
  <assign operator="=">
    <left>
      <identifier name="i"/>
    </left>
    <right>
      <identifier name="b"/>
    </right>
  </assign>
</program>
"""
        ),
        (
        r"""
        i.a = "b";
        """,
"""
<program>
  <assign operator="=">
    <left>
      <dotaccessor>
        <object>
          <identifier name="i"/>
        </object>
        <property>
          <identifier name="a"/>
        </property>
      </dotaccessor>
    </left>
    <right>
      <string>b</string>
    </right>
  </assign>
</program>
"""
        ),
        (
        r"""
        i["a"] = "b";
        """,
"""
<program>
  <assign operator="=">
    <left>
      <bracketaccessor>
        <object>
          <identifier name="i"/>
        </object>
        <property>
          <string>a</string>
        </property>
      </bracketaccessor>
    </left>
    <right>
      <string>b</string>
    </right>
  </assign>
</program>
"""
        ),
        (
        r"""
        i[a] = "b";
        """,
"""
<program>
  <assign operator="=">
    <left>
      <bracketaccessor>
        <object>
          <identifier name="i"/>
        </object>
        <property>
          <identifier name="a"/>
        </property>
      </bracketaccessor>
    </left>
    <right>
      <string>b</string>
    </right>
  </assign>
</program>
"""
        ),

        # control structures
        (
        r"""
        if (condition) {
            result = expression;
        }""",
"""
<program>
  <if>
    <predicate>
      <identifier name="condition"/>
    </predicate>
    <then>
      <block>
        <assign operator="=">
          <left>
            <identifier name="result"/>
          </left>
          <right>
            <identifier name="expression"/>
          </right>
        </assign>
      </block>
    </then>
  </if>
</program>
"""
        ),
        (
        r"""
        if (condition) {
            result = expression;
        } else {
            result = alternative;
        }""",
"""
<program>
  <if>
    <predicate>
      <identifier name="condition"/>
    </predicate>
    <then>
      <block>
        <assign operator="=">
          <left>
            <identifier name="result"/>
          </left>
          <right>
            <identifier name="expression"/>
          </right>
        </assign>
      </block>
    </then>
    <else>
      <block>
        <assign operator="=">
          <left>
            <identifier name="result"/>
          </left>
          <right>
            <identifier name="alternative"/>
          </right>
        </assign>
      </block>
    </else>
  </if>
</program>
"""
        ),

        (
        r"""
        if (exprA == exprB) {
           result = expression;
        } else if (expr2) {
           result = alternative1;
        } else {
           result = alternative2;
        }""",
"""
<program>
  <if>
    <predicate>
      <binaryoperation operation="==">
        <left>
          <identifier name="exprA"/>
        </left>
        <right>
          <identifier name="exprB"/>
        </right>
      </binaryoperation>
    </predicate>
    <then>
      <block>
        <assign operator="=">
          <left>
            <identifier name="result"/>
          </left>
          <right>
            <identifier name="expression"/>
          </right>
        </assign>
      </block>
    </then>
    <else>
      <if>
        <predicate>
          <identifier name="expr2"/>
        </predicate>
        <then>
          <block>
            <assign operator="=">
              <left>
                <identifier name="result"/>
              </left>
              <right>
                <identifier name="alternative1"/>
              </right>
            </assign>
          </block>
        </then>
        <else>
          <block>
            <assign operator="=">
              <left>
                <identifier name="result"/>
              </left>
              <right>
                <identifier name="alternative2"/>
              </right>
            </assign>
          </block>
        </else>
      </if>
    </else>
  </if>
</program>
"""
        ),

        (
        "result = condition ? expression : alternative;",
"""
<program>
  <assign operator="=">
    <left>
      <identifier name="result"/>
    </left>
    <right>
      <conditional>
        <condition>
          <identifier name="condition"/>
        </condition>
        <value1>
          <identifier name="expression"/>
        </value1>
        <value2>
          <identifier name="alternative"/>
        </value2>
      </conditional>
    </right>
  </assign>
</program>
"""
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
"""
<program>
  <switch>
    <expression>
      <identifier name="expr"/>
    </expression>
    <case>
      <expression>
        <identifier name="SOMEVALUE"/>
      </expression>
      <break/>
    </case>
    <case>
      <expression>
        <identifier name="ANOTHERVALUE"/>
      </expression>
      <break/>
    </case>
    <default>
      <break/>
    </default>
  </switch>
</program>
"""
        ),

        # for loop
        (
        r"""
        for (var i = 0; i < 5; i++) {
            a = i;
        }
        """,
"""
<program>
  <for>
    <init>
      <var name="i">
        <number value="0"/>
      </var>
    </init>
    <condition>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="i"/>
        </left>
        <right>
          <number value="5"/>
        </right>
      </binaryoperation>
    </condition>
    <post>
      <postfix operation="++">
        <identifier name="i"/>
      </postfix>
    </post>
    <statement>
      <block>
        <assign operator="=">
          <left>
            <identifier name="a"/>
          </left>
          <right>
            <identifier name="i"/>
          </right>
        </assign>
      </block>
    </statement>
  </for>
</program>
"""
        ),
        (
        r"""
        for (var i = 0; i < 5; i++) {
            a = i
        }
        """,
"""
<program>
  <for>
    <init>
      <var name="i">
        <number value="0"/>
      </var>
    </init>
    <condition>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="i"/>
        </left>
        <right>
          <number value="5"/>
        </right>
      </binaryoperation>
    </condition>
    <post>
      <postfix operation="++">
        <identifier name="i"/>
      </postfix>
    </post>
    <statement>
      <block>
        <assign operator="=">
          <left>
            <identifier name="a"/>
          </left>
          <right>
            <identifier name="i"/>
          </right>
        </assign>
      </block>
    </statement>
  </for>
</program>
"""
        ),
        (
        r"""
        for (var key in array) {
            continue;
        }
        """,
"""
<program>
  <forin>
    <variable>
      <var name="key"/>
    </variable>
    <object>
      <identifier name="array"/>
    </object>
    <statement>
      <block>
        <continue/>
      </block>
    </statement>
  </forin>
</program>
"""
        ),
        (
        r"""
        for (;;) {
            break;
        }
        """,
"""
<program>
  <for>
    <statement>
      <block>
        <break/>
      </block>
    </statement>
  </for>
</program>
"""
        ),
        (
        r"""
        for (; i < len; i++) {
            j = i;
        }
        """,
"""
<program>
  <for>
    <condition>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="i"/>
        </left>
        <right>
          <identifier name="len"/>
        </right>
      </binaryoperation>
    </condition>
    <post>
      <postfix operation="++">
        <identifier name="i"/>
      </postfix>
    </post>
    <statement>
      <block>
        <assign operator="=">
          <left>
            <identifier name="j"/>
          </left>
          <right>
            <identifier name="i"/>
          </right>
        </assign>
      </block>
    </statement>
  </for>
</program>
"""
        ),
        (
        r"""
        for (var i = 0, len = cars.length, text = ""; i < len; i++) {
            text += cars[i] + "<br>";
        }
        """,
"""
<program>
  <for>
    <init>
      <var name="i">
        <number value="0"/>
      </var>
      <var name="len">
        <dotaccessor>
          <object>
            <identifier name="cars"/>
          </object>
          <property>
            <identifier name="length"/>
          </property>
        </dotaccessor>
      </var>
      <var name="text">
        <string></string>
      </var>
    </init>
    <condition>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="i"/>
        </left>
        <right>
          <identifier name="len"/>
        </right>
      </binaryoperation>
    </condition>
    <post>
      <postfix operation="++">
        <identifier name="i"/>
      </postfix>
    </post>
    <statement>
      <block>
        <assign operator="+=">
          <left>
            <identifier name="text"/>
          </left>
          <right>
            <binaryoperation operation="+">
              <left>
                <bracketaccessor>
                  <object>
                    <identifier name="cars"/>
                  </object>
                  <property>
                    <identifier name="i"/>
                  </property>
                </bracketaccessor>
              </left>
              <right>
                <string>&lt;br&gt;</string>
              </right>
            </binaryoperation>
          </right>
        </assign>
      </block>
    </statement>
  </for>
</program>
"""
        ),
        (
        """
        for (; i < len; ) {
            text += cars[i] + "<br>";
            i++;
        }
        """,
"""
<program>
  <for>
    <condition>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="i"/>
        </left>
        <right>
          <identifier name="len"/>
        </right>
      </binaryoperation>
    </condition>
    <statement>
      <block>
        <assign operator="+=">
          <left>
            <identifier name="text"/>
          </left>
          <right>
            <binaryoperation operation="+">
              <left>
                <bracketaccessor>
                  <object>
                    <identifier name="cars"/>
                  </object>
                  <property>
                    <identifier name="i"/>
                  </property>
                </bracketaccessor>
              </left>
              <right>
                <string>&lt;br&gt;</string>
              </right>
            </binaryoperation>
          </right>
        </assign>
        <postfix operation="++">
          <identifier name="i"/>
        </postfix>
      </block>
    </statement>
  </for>
</program>
"""
        ),

        # while loop
        (
        """
        while (a<b) {
           a+=1;
        }
        """,
"""
<program>
  <while>
    <predicate>
      <binaryoperation operation="&lt;">
        <left>
          <identifier name="a"/>
        </left>
        <right>
          <identifier name="b"/>
        </right>
      </binaryoperation>
    </predicate>
    <statement>
      <block>
        <assign operator="+=">
          <left>
            <identifier name="a"/>
          </left>
          <right>
            <number value="1"/>
          </right>
        </assign>
      </block>
    </statement>
  </while>
</program>
"""
        ),
        (
        """
        do {
           a+=1;
         } while (a<b);
        """,
"""
<program>
  <statement>
    <block>
      <assign operator="+=">
        <left>
          <identifier name="a"/>
        </left>
        <right>
          <number value="1"/>
        </right>
      </assign>
    </block>
  </statement>
  <while>
    <binaryoperation operation="&lt;">
      <left>
        <identifier name="a"/>
      </left>
      <right>
        <identifier name="b"/>
      </right>
    </binaryoperation>
  </while>
</program>
"""
        ),

        # with
        (
        """
        with (document) {
           var a = getElementById('a');
           var b = getElementById('b');
           var c = getElementById('c');
           var c = document.get('c');
         };
        """,
"""
<program>
  <with>
    <identifier name="document"/>
    <statement>
      <block>
        <var name="a">
          <functioncall>
            <function>
              <identifier name="getElementById"/>
            </function>
            <arguments>
              <string>a</string>
            </arguments>
          </functioncall>
        </var>
        <var name="b">
          <functioncall>
            <function>
              <identifier name="getElementById"/>
            </function>
            <arguments>
              <string>b</string>
            </arguments>
          </functioncall>
        </var>
        <var name="c">
          <functioncall>
            <function>
              <identifier name="getElementById"/>
            </function>
            <arguments>
              <string>c</string>
            </arguments>
          </functioncall>
        </var>
        <var name="c">
          <functioncall>
            <function>
              <dotaccessor>
                <object>
                  <identifier name="document"/>
                </object>
                <property>
                  <identifier name="get"/>
                </property>
              </dotaccessor>
            </function>
            <arguments>
              <string>c</string>
            </arguments>
          </functioncall>
        </var>
      </block>
    </statement>
  </with>
  <empty>;</empty>
</program>
"""
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
"""
<program>
  <label name="loop1">
    <statement>
      <for>
        <init>
          <var name="a">
            <number value="0"/>
          </var>
        </init>
        <condition>
          <binaryoperation operation="&lt;">
            <left>
              <identifier name="a"/>
            </left>
            <right>
              <number value="10"/>
            </right>
          </binaryoperation>
        </condition>
        <post>
          <postfix operation="++">
            <identifier name="a"/>
          </postfix>
        </post>
        <statement>
          <block>
            <if>
              <predicate>
                <binaryoperation operation="==">
                  <left>
                    <identifier name="a"/>
                  </left>
                  <right>
                    <number value="4"/>
                  </right>
                </binaryoperation>
              </predicate>
              <then>
                <block>
                  <break>
                    <identifier name="loop1"/>
                  </break>
                </block>
              </then>
            </if>
            <functioncall>
              <function>
                <identifier name="alert"/>
              </function>
              <arguments>
                <binaryoperation operation="+">
                  <left>
                    <string>a = </string>
                  </left>
                  <right>
                    <identifier name="a"/>
                  </right>
                </binaryoperation>
              </arguments>
            </functioncall>
            <label name="loop2">
              <statement>
                <for>
                  <init>
                    <var name="b">
                      <number value="0"/>
                    </var>
                  </init>
                  <condition>
                    <binaryoperation operation="&lt;">
                      <left>
                        <identifier name="b"/>
                      </left>
                      <right>
                        <number value="10"/>
                      </right>
                    </binaryoperation>
                  </condition>
                  <post>
                    <unaryoperation operation="++">
                      <identifier name="b"/>
                    </unaryoperation>
                  </post>
                  <statement>
                    <block>
                      <if>
                        <predicate>
                          <binaryoperation operation="==">
                            <left>
                              <identifier name="b"/>
                            </left>
                            <right>
                              <number value="3"/>
                            </right>
                          </binaryoperation>
                        </predicate>
                        <then>
                          <block>
                            <continue>
                              <identifier name="loop2"/>
                            </continue>
                          </block>
                        </then>
                      </if>
                      <if>
                        <predicate>
                          <binaryoperation operation="==">
                            <left>
                              <identifier name="b"/>
                            </left>
                            <right>
                              <number value="6"/>
                            </right>
                          </binaryoperation>
                        </predicate>
                        <then>
                          <block>
                            <continue>
                              <identifier name="loop1"/>
                            </continue>
                          </block>
                        </then>
                      </if>
                      <functioncall>
                        <function>
                          <identifier name="alert"/>
                        </function>
                        <arguments>
                          <binaryoperation operation="+">
                            <left>
                              <string>b = </string>
                            </left>
                            <right>
                              <identifier name="b"/>
                            </right>
                          </binaryoperation>
                        </arguments>
                      </functioncall>
                    </block>
                  </statement>
                </for>
              </statement>
            </label>
            <functioncall>
              <function>
                <identifier name="alert"/>
              </function>
              <arguments>
                <string>finished</string>
              </arguments>
            </functioncall>
          </block>
        </statement>
      </for>
    </statement>
  </label>
  <label name="block1">
    <statement>
      <block>
        <functioncall>
          <function>
            <identifier name="alert"/>
          </function>
          <arguments>
            <string>hello</string>
          </arguments>
        </functioncall>
        <break>
          <identifier name="block1"/>
        </break>
        <functioncall>
          <function>
            <identifier name="alert"/>
          </function>
          <arguments>
            <string>world</string>
          </arguments>
        </functioncall>
      </block>
    </statement>
  </label>
</program>
"""
        ),

        # functions
        (
        """
        function foo(p) {
            p = "bar";
        }
        """,
"""
<program>
  <funcdecl name="foo">
    <parameters>
      <identifier name="p"/>
    </parameters>
    <body>
      <assign operator="=">
        <left>
          <identifier name="p"/>
        </left>
        <right>
          <string>bar</string>
        </right>
      </assign>
    </body>
  </funcdecl>
</program>
"""
        ),
        (
        """
        function hello() {
            alert('world');
        }
        """,
"""
<program>
  <funcdecl name="hello">
    <parameters/>
    <body>
      <functioncall>
        <function>
          <identifier name="alert"/>
        </function>
        <arguments>
          <string>world</string>
        </arguments>
      </functioncall>
    </body>
  </funcdecl>
</program>
"""
        ),
        (
        """
        var anon = function() {
            alert('I am anonymous');
        };
        """,
"""
<program>
  <var name="anon">
    <funcexpr>
      <identifier/>
      <parameters/>
      <body>
        <functioncall>
          <function>
            <identifier name="alert"/>
          </function>
          <arguments>
            <string>I am anonymous</string>
          </arguments>
        </functioncall>
      </body>
    </funcexpr>
  </var>
</program>
"""
        ),
        (
        """
        anon();
        """,
"""
<program>
  <functioncall>
    <function>
      <identifier name="anon"/>
    </function>
    <arguments/>
  </functioncall>
</program>
"""
        ),
        (
        """
        setTimeout(function() {
            alert('hello');
        }, 1000)
        """,
"""
<program>
  <functioncall>
    <function>
      <identifier name="setTimeout"/>
    </function>
    <arguments>
      <funcexpr>
        <identifier/>
        <parameters/>
        <body>
          <functioncall>
            <function>
              <identifier name="alert"/>
            </function>
            <arguments>
              <string>hello</string>
            </arguments>
          </functioncall>
        </body>
      </funcexpr>
      <number value="1000"/>
    </arguments>
  </functioncall>
</program>
"""
        ),
        (
        """
        (function() {
            alert('foo');
        }());
        """,
"""
<program>
  <functioncall>
    <function>
      <funcexpr>
        <identifier/>
        <parameters/>
        <body>
          <functioncall>
            <function>
              <identifier name="alert"/>
            </function>
            <arguments>
              <string>foo</string>
            </arguments>
          </functioncall>
        </body>
      </funcexpr>
    </function>
    <arguments/>
  </functioncall>
</program>
"""
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
"""
<program>
  <var name="obj">
    <object>
      <get>
        <property>
          <identifier name="latest"/>
        </property>
        <body>
          <return>
            <string>latest</string>
          </return>
        </body>
      </get>
    </object>
  </var>
</program>
"""
        ),
        (
        """
        delete obj.latest;
        """,
"""
<program>
  <unaryoperation operation="delete">
    <dotaccessor>
      <object>
        <identifier name="obj"/>
      </object>
      <property>
        <identifier name="latest"/>
      </property>
    </dotaccessor>
  </unaryoperation>
</program>
"""
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
"""
<program>
  <var name="o">
    <object>
      <set>
        <body>
          <return>
            <assign operator="=">
              <left>
                <bracketaccessor>
                  <object>
                    <dotaccessor>
                      <object>
                        <identifier>this</identifier>
                      </object>
                      <property>
                        <identifier name="log"/>
                      </property>
                    </dotaccessor>
                  </object>
                  <property>
                    <dotaccessor>
                      <object>
                        <dotaccessor>
                          <object>
                            <identifier>this</identifier>
                          </object>
                          <property>
                            <identifier name="log"/>
                          </property>
                        </dotaccessor>
                      </object>
                      <property>
                        <identifier name="length"/>
                      </property>
                    </dotaccessor>
                  </property>
                </bracketaccessor>
              </left>
              <right>
                <identifier name="str"/>
              </right>
            </assign>
          </return>
        </body>
      </set>
      <property name="log">
        <array/>
      </property>
    </object>
  </var>
</program>
"""
        ),

    ]

    for snippet, expected in jscode_snippets:
        print "---------------------------------------------------------"
        print snippet
        js = js2xml.parse(snippet)
        output = js2xml.pretty_print(js).strip()
        assert_equal(output, expected.strip(), "got\n%s\nexpected:\n%s" % (output, expected))
