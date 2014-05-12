js2xml XML schema by example
============================

All examples are taken from https://en.wikibooks.org/wiki/JavaScript/Variables_and_Types

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


Complex types
-------------

Array Type
**********

Using the statement new followed by ``Array``:

.. code:: javascript

    var myArray = new Array(0, 2, 4);
    var myOtherArray = new Array();

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>myArray</identifier>
      <initializer>
        <new>
          <identifier>Array</identifier>
          <arguments>
            <number>0</number>
            <number>2</number>
            <number>4</number>
          </arguments>
        </new>
      </initializer>
    </var_decl>
  </var>
  <var>
    <var_decl>
      <identifier>myOtherArray</identifier>
      <initializer>
        <new>
          <identifier>Array</identifier>
          <arguments/>
        </new>
      </initializer>
    </var_decl>
  </var>


Arrays can also be created with the array notation, which uses square brackets:

.. code:: javascript

    var myArray = [0, 2, 4];
    var myOtherArray = [];

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>myArray</identifier>
      <initializer>
        <array>
          <number>0</number>
          <number>2</number>
          <number>4</number>
        </array>
      </initializer>
    </var_decl>
  </var>
  <var>
    <var_decl>
      <identifier>myOtherArray</identifier>
      <initializer>
        <array/>
      </initializer>
    </var_decl>
  </var>


Arrays are accessed using the square brackets:

.. code:: javascript

    myArray[2] = "Hello";
    var text = myArray[2];

becomes

.. code:: xml

  <assign>
    <left>
      <bracketaccessor>
        <object>
          <identifier>myArray</identifier>
        </object>
        <property>
          <number>2</number>
        </property>
      </bracketaccessor>
    </left>
    <operator>=</operator>
    <right>
      <string>Hello</string>
    </right>
  </assign>
  <var>
    <var_decl>
      <identifier>text</identifier>
      <initializer>
        <bracketaccessor>
          <object>
            <identifier>myArray</identifier>
          </object>
          <property>
            <number>2</number>
          </property>
        </bracketaccessor>
      </initializer>
    </var_decl>
  </var>


Object Types
************

Using the ``new`` operator:

.. code:: javascript

    var myObject = new Object();

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>myObject</identifier>
      <initializer>
        <new>
          <identifier>Object</identifier>
          <arguments/>
        </new>
      </initializer>
    </var_decl>
  </var>

Using curly braces notation:

.. code:: javascript

    var myObject = {};

becomes

.. code:: xml

  <var>
    <var_decl>
      <identifier>myObject</identifier>
      <initializer>
        <object/>
      </initializer>
    </var_decl>
  </var>

