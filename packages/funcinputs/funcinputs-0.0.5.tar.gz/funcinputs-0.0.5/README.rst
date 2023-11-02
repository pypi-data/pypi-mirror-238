==========
funcinputs
==========

Overview
--------

The funcinputs project holds the class FuncInput. The objects of this class represent the entire input that can be passed to a function when the function is called. Each FuncInput object has a list of positional arguments (the property is called `args`) and a dict of keyword arguments (the property is called `kwargs`). One can do everything with a FuncInput object that can be done with a list or a dict e.g. indexers, appending, or updating.

Installation
------------

To install funcinputs, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install funcinputs

Usage
-----

Once funcinputs is installed, you can use it as follows:

.. code-block:: python

    from funcinputs import FuncInput

    x = FuncInput(args=[9, "foo"], kwargs={"bar":12.75})
    print(x) # FuncInput(args=[9, 'foo'], kwargs={'bar': 12.75})
    x += FuncInput(args=[2], kwargs={"baz":"spam"})
    print(x) # FuncInput(args=[9, 'foo', 2], kwargs={'bar': 12.75, 'baz': 'spam'})
    x.append(19)
    print(x) # FuncInput(args=[9, 'foo', 2, 19], kwargs={'bar': 12.75, 'baz': 'spam'})

License
-------

This project is licensed under the MIT License.

Credits
-------

- Author: Aaron Alphabet
- Email: aaron.alphabet@posteo.org

Thank you for using funcinputs!

