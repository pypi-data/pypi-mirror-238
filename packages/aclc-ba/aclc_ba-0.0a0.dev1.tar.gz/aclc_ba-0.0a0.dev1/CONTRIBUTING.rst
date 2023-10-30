Contributing
============


Code Guidelines
---------------
- ensure that code works with Python ... or later
- maintain high-quality coding standards; follow    `PEP8 <https://peps.python.org/pep-0008/>`_ Style for code.

Indentation:
^^^^^^^^^^^^
* Each indentation level is 4 spaces (no tabs).
* Arguments should be aligned with the opening delimiter as in the first example `PEP8 indentation section <https://peps.python.org/pep-0008/#indentation>`_.
* If arguments are to be split into multiple lines, there should only be one argument per line.

Pre-Commit Hooks:
^^^^^^^^^^^^
* After cloning the repo, after installing the packages from `requirements.txt`, enter the repo folder and run `pre-commit install`.
Each time a `git commit` is initiated, `black`  will run automatically on the modified files only.
In case of error, the modified file needs to be `git add` once again and a new `git commit` has to be issued.

Strings:
^^^^^^^^
* Always using single-quoted strings except for docstrings (as per `PEP8 <https://www.python.org/dev/peps/pep-0008/#string-quotes>`_).
* Use the new string formatting API ``'{}'.format(x)`` instead of ``'%s' % (x,)``
  (\ `see here for more information <https://pyformat.info/>`_\ ).

Naming Conventions:
^^^^^^^^^^^^^^^^^^^

* Classes are always in camel case (eg. `SomeClass`).
* Variables, functions, and methods are always mixed case (eg. `someVar`)

Source Files
^^^^^^^^^^^^

All Python source files should be UTF-8 encoded with the UTF-8 header on top
like so:

.. code-block:: python

   # -*- coding: utf-8 -*-

Standalone scripts should also have a hashbang header like so:

.. code-block:: python

   #!/usr/bin/env python
   # -*- coding: utf-8 -*-

Setting Up a Development Environment
====================================


Tests
=====

Git and our Branching model
===========================

