js2xml XML schema by example
============================

Variable declaration
--------------------

Explicit decleration
********************

.. code:: javascript

    var c;
  
becomes

.. code:: xml

    <program>
      <var>
        <var_decl>
          <identifier>c</identifier>
        </var_decl>
      </var>
    </program>


Initialized declaration
***********************

.. code:: javascript

    var c = 0;
  
becomes

.. code:: xml

    <program>
      <var>
        <var_decl>
          <identifier>c</identifier>
          <initializer>
            <number>0</number>
          </initializer>
        </var_decl>
      </var>
    </program>


Assigning a value
*****************

.. code:: javascript

    c = 1;

becomes


.. code:: xml

    <program>
      <assign>
        <left>
          <identifier>c</identifier>
        </left>
        <operator>=</operator>
        <right>
          <number>1</number>
        </right>
      </assign>
    </program>
