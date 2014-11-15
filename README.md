js2xml
======

[![Build Status](https://travis-ci.org/redapple/js2xml.png?branch=master)](https://travis-ci.org/redapple/js2xml)

Convert Javascript code to an XML document.

This makes it easy to extract data embedded in JavaScript code using XPath
in a way more robust than just using regular expressions.


# Install:

You can install js2xml via [PyPI](https://pypi.python.org/pypi/js2xml):

    pip install js2xml


# Example:

```python
>>> import js2xml
>>>
>>> jscode = """function factorial(n) {
...     if (n === 0) {
...         return 1;
...     }
...     return n * factorial(n - 1);
... }"""
>>> parsed = js2xml.parse(jscode)
>>>
>>> parsed.xpath("//funcdecl/@name")  # extracts function name
['factorial']
>>>
>>> print js2xml.pretty_print(parsed)  # pretty-print generated XML
<program>
  <funcdecl name="factorial">
    <parameters>
      <identifier name="n"/>
    </parameters>
    <body>
      <if>
        <predicate>
          <binaryoperation operation="===">
            <left>
              <identifier name="n"/>
            </left>
            <right>
              <number value="0"/>
            </right>
          </binaryoperation>
        </predicate>
        <then>
          <block>
            <return>
              <number value="1"/>
            </return>
          </block>
        </then>
      </if>
      <return>
        <binaryoperation operation="*">
          <left>
            <identifier name="n"/>
          </left>
          <right>
            <functioncall>
              <function>
                <identifier name="factorial"/>
              </function>
              <arguments>
                <binaryoperation operation="-">
                  <left>
                    <identifier name="n"/>
                  </left>
                  <right>
                    <number value="1"/>
                  </right>
                </binaryoperation>
              </arguments>
            </functioncall>
          </right>
        </binaryoperation>
      </return>
    </body>
  </funcdecl>
</program>

>>>


```
