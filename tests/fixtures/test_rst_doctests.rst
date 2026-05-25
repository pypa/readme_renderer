========
doctests
========

Looking for https://pygments.org/docs/lexers/#pygments.lexers.python.PythonConsoleLexer

--------
docutils
--------

raw
===

No indentation, no directive, just the code block of a repl session.

>>> a = 'foo'
>>> print(a)
foo 
>>> 1 / 0
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
ZeroDivisionError: integer division or modulo by zero

code
====

With the "code" directive, the content is indented and a lexer is specified.

.. code:: pycon

   >>> a = 'foo'
   >>> print(a)
   foo 
   >>> 1 / 0
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ZeroDivisionError: integer division or modulo by zero

References:

- https://docutils.sourceforge.io/docs/ref/rst/directives.html#code

And without a lexer:

.. code::

   >>> a = 'foo'
   >>> print(a)
   foo 
   >>> 1 / 0
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ZeroDivisionError: integer division or modulo by zero


------
sphinx
------

raw - expect the same, as not using any sphinx extension.


code-block
==========

.. code-block:: pycon

   >>> a = 'foo'
   >>> print(a)
   foo 
   >>> 1 / 0
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ZeroDivisionError: integer division or modulo by zero

References:

- https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
