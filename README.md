js2xml
======

Convert Javascript code to an XML document

Example:

```python
>>> import js2xml
>>> import lxml.etree
>>>
>>> jscode = """function factorial(n) {
...     if (n === 0) {
...         return 1;
...     }
...     return n * factorial(n - 1);
... }"""
>>> jsxml = js2xml.parse(jscode)
>>>
>>> print jsxml
<Element program at 0x7fb3f7280050>

>>> print lxml.etree.tostring(jsxml, pretty_print=True)
<program>
  <funcdecl>
    <identifier>factorial</identifier>
    <parameters>
      <identifier>n</identifier>
    </parameters>
    <body>
      <if>
        <predicate>
          <binaryoperation>
            <left>
              <identifier>n</identifier>
            </left>
            <operator>===</operator>
            <right>
              <number>0</number>
            </right>
          </binaryoperation>
        </predicate>
        <then>
          <block>
            <return>
              <number>1</number>
            </return>
          </block>
        </then>
      </if>
      <return>
        <binaryoperation>
          <left>
            <identifier>n</identifier>
          </left>
          <operator>*</operator>
          <right>
            <functioncall>
              <identifier>
                <identifier>factorial</identifier>
              </identifier>
              <arguments>
                <binaryoperation>
                  <left>
                    <identifier>n</identifier>
                  </left>
                  <operator>-</operator>
                  <right>
                    <number>1</number>
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
