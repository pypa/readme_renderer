Here is some Python code for a ``Dog``:

.. code-block:: python

    class Dog(Animal):
        def __init__(self, name):
            self.name = name

        def make_sound(self):
            print('Ruff!')

    dog = Dog('Fido')

and then here is some bash:

.. code-block:: bash

    if [ "$1" = "--help" ]; then
        echo "OK"
    fi

or click `SurveyMonkey <http://www.surveymonkey.com>`_

and an ignored Sphinx option:

.. code-block:: python
   :caption: Naive Fibonacci computation

    def fib(n):
        if n < 1:
            return 0
        elif n <= 2:
            return 1

        return fib(n - 1) + fib(n - 2)
