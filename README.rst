Lydoc - A Lilypond API documentation generator
##############################################

.. image:: https://img.shields.io/pypi/v/lydoc.svg?maxAge=86400   
   :target: https://pypi.python.org/pypi/lydoc
   :alt: PyPI Package
.. image:: http://readthedocs.org/projects/lydoc/badge/?version=latest
   :target: http://lydoc.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://travis-ci.org/Cecca/lydoc.svg?branch=master
   :target: https://travis-ci.org/Cecca/lydoc
   :alt: Continuous Integration

..
   The marker below is used to tell Sphinx where to start
   to include the README file into the main documentation

.. inclusion-marker

Lydoc is a software that looks for documentation comments in `GNU
Lilypond`_ source files, and outputs API documentation in a variety of
formats.

-----------------------------------------------------------------------

Installation
============

Lydoc works with both Python 2 (version 2.7 is supported) and Python 3
(versions 3.3, 3.4, and 3.5). You can install it in several ways.

From source
-----------

Clone the repository somewhere on your machine. To install, run from
the root directory of the project::

  python setup.py install

which will install the ``lydoc`` executable, while fetching all the
necessary dependencies in the process. To upgrade, just pull the
latest changes and run the above command again.

From PyPI
---------

Lydoc is also available on the Python Package Index. You can install
it with this single command::

  pip install --user lydoc

I recommend running the above command with the ``--user`` option so
not to mess with system packages. If you omit the ``--user`` argument,
you might require administration privileges, depending on you
machine's configuration.

To upgrade, it is sufficient to run the following command::

  pip install --user --upgrade lydoc

Very quick start
================

Just run the following command::

  lydoc -o api.rst file.ly

to collect documentation from ``file.ly`` and write a ``api.rst`` text
file formatted with `reStructuredText`_.

Quick start
===========

Lydoc will look for documentation comments in the given file or
directory. In the latter case, it will parse all ``.ly`` and ``.ily``
files, recursively. A documentation comment looks like a standard
Lilypond block comment, with a slightly different opening::

  %{!
  % I am a documentation comment :-)
  %}
  someFunction =
  #(define-music-function ...)

Note the ``!`` character after the opening of the comment: that's the
character that Lydoc uses to distinguish between normal block comments
and documentation ones.

So, to extract the documentation from a single file, the command line
is the following::

  lydoc file.ly

This will output some logging information to standard error, and the
collected documentation on standard output, as a stream of JSON
objects, one per line. This is useful to pipe the output of Lydoc to
some other program, in a machine-friendly format.

However, we are humans, not machines, hence we might want to generate
something more readable, like a file in some lightweight markup
language. You have some options:

`Markdown`_
  Arguably the most widespread lightweight markup language::
    
    lydoc -o api.md file.ly

`reStructuredText`_
  The markup language used by the powerful `Sphinx`_
  documentation generator::

    lydoc -o api.rst file.ly

For more detailed usage instructions, head to the :doc:`/user-manual`
page.


.. _`GNU Lilypond`: http://lilypond.org/
.. _reStructuredText: http://www.sphinx-doc.org/en/stable/rest.html
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
