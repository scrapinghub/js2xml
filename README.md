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


# Changelog

## v0.2.1 (2016-06-10)

- Distribute as universal wheel

## v0.2.0 (2016-06-10)

- Python 3 support (tested with 3.4 and 3.5)
- Use logger to suppress Yacc warnings
- require PLY > 3.6
- Use bumpversion for versioning
- Pretty-print output is now a Unicode string

## v0.1.2 (2015-05-11)

- Profiling scripts added
- Updated notes with use-case, installing via pip
- Force PLY 3.4 (3.6 has issues with slimit)

## v0.1.1 (2014-08-13)

- Fix parsing of objects with integer keys
- Fix try/catch/finally and named function expressions
- Add download URL in setup file (for PyPI)

## v0.1 (2014-08-12)

Initial release
