js2xml XML schema by example
============================

Variable declaration
--------------------

Explicit declaration
********************

.. code:: javascript

    var c;
  
becomes

.. code:: xml

      <var>
        <var_decl>
          <identifier>c</identifier>
        </var_decl>
      </var>


Initialized declaration
***********************

.. code:: javascript

    var c = 0;
  
becomes

.. code:: xml


      <var>
        <var_decl>
          <identifier>c</identifier>
          <initializer>
            <number>0</number>
          </initializer>
        </var_decl>
      </var>


Assigning a value
*****************

.. code:: javascript

    c = 1;

becomes


.. code:: xml


      <assign>
        <left>
          <identifier>c</identifier>
        </left>
        <operator>=</operator>
        <right>
          <number>1</number>
        </right>
      </assign>



Primitive types
---------------

Boolean type
************

.. code:: javascript

    var mayday = false;
    var birthday = true;
  
becomes

.. code:: xml

    <var>
        <var_decl>
          <identifier>mayday</identifier>
          <initializer>
            <boolean>false</boolean>
          </initializer>
        </var_decl>
        </var>
        <var>
        <var_decl>
          <identifier>birthday</identifier>
          <initializer>
            <boolean>true</boolean>
          </initializer>
        </var_decl>
    </var>


Numeric types
*************

.. code:: javascript

    var sal = 20;
    var pal = 12.1;

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>sal</identifier>
      <initializer>
        <number>20</number>
      </initializer>
    </var_decl>
  </var>
  <var>
    <var_decl>
      <identifier>pal</identifier>
      <initializer>
        <number>12.1</number>
      </initializer>
    </var_decl>
  </var>


String type
***********

.. code:: javascript

    var myName = "Some Name";
    var myChar = 'f';

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>myName</identifier>
      <initializer>
        <string>Some Name</string>
      </initializer>
    </var_decl>
  </var>
  <var>
    <var_decl>
      <identifier>myChar</identifier>
      <initializer>
        <string>f</string>
      </initializer>
    </var_decl>
  </var>
