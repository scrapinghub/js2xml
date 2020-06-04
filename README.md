js2xml
======

[![Build Status](https://travis-ci.org/scrapinghub/js2xml.png?branch=master)](https://travis-ci.org/scrapinghub/js2xml)
[![codecov](https://codecov.io/gh/scrapinghub/js2xml/branch/master/graph/badge.svg)](https://codecov.io/gh/scrapinghub/js2xml)

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
>>> print(js2xml.pretty_print(parsed))  # pretty-print generated XML
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

## v0.4.0 (2020-06-04)

- Add Python 3.7 and 3.8 support, drop Python 3.4 support

- Use `calmjs.parse` instead of `slimit` for JavaScript parsing

  [`calmjs.parse`](https://github.com/calmjs/calmjs.parse) is a well-maintained
  fork of [`slimit`](https://github.com/rspivak/slimit) which solves some of
  its shortcomings, such as support for JavaScript keywords being used as
  object keys.

  However, `calmjs.parse` also introduces slight changes to the output of
  js2xml, making this change backward-incompatible.

- Fix unicode surrogate pair handling

- Code cleanup for Python 3

## v0.3.1 (2017-08-03)

- Fix packaging

## v0.3.0 (2017-08-03)

- Add Python 3.6 support
- Deprecate `js2xml.jsonlike`
- Introduce `js2xml.utils.objects` module:

  - `js2xml.utils.objects.make(node)`: takes a node in the js2xml-parsed
    tree and converts to a suitable Python object
  - `js2xml.utils.objects.findall(tree, types)`: used to find the
    top-most nodes in the js2xml-parsed tree that can be converted to
    a `dict`, `list`, `str`, `bool`, `int` or `float`
  - `js2xml.utils.objects.getall(tree, types)`: same as `.findall()`
    except that it converts what was found to the corresponding Python
    object, using `js2xml.utils.objects.make()`

- Introduce `js2xml.utils.vars` module:

  - `js2xml.utils.vars.get_vars(tree)` can be used to turn a JS snippet
    into a python object where you can access JavaScript variables
    by name and get the parsed values

## v0.2.3 (2017-05-30)

- Regenerate lextab.py and yacctab.py files with PLY 3.10
- Properly set logger level to ERROR

## v0.2.2 (2016-12-01)

- Include lextab.py and yacctab.py files to (hopefully) remove write
  permission warnings (see issue #16)
- Run tests with tox (locally and on Travis CI)
- Add code coverage reports (+ codecov.io for Travis CI builds)
- Run tests with Python 3.6
- Automatic PyPI deploys from Travis CI

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
