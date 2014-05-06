js2xml
======

Convert Javascript code to an XML document

Example:

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
>>> print js2xml.pretty_print(parsed)
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
