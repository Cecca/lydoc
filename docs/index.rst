.. Lydoc documentation master file, created by
   sphinx-quickstart on Wed Apr 20 22:55:28 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

########################################
Lydoc - Lilypond documentation generator
########################################

Lydoc is a software to extract documentation from `GNU Lilypond`_ files. It can
be used to generate documentation for reusable Lilypond libraries.

.. _`GNU Lilypond`: http://lilypond.org/


**Contents**:

.. toctree::
   :maxdepth: 2

   user-manual

Installation
============

From source
-----------

Lydoc requires python3. To install, run from the root directory of the
project::

    python3 setup.py install

which will install all the necessary dependencies.

Quick start
===========

To generate API documentation for a single lilypond file in
`reStructuredText`_ format::

    lydoc -o api.rst file.ly

or in `Markdown`_::

    lydoc -o api.md file.ly


You can also generate API documentation for all Lilypond files in a
given directory, recursively::

    lydoc -o api.rst directory


For more detailed usage instructions, head to the :doc:`/user-manual`
page.


.. _reStructuredText: http://www.sphinx-doc.org/en/stable/rest.html
.. _Markdown: http://daringfireball.net/projects/markdown/



..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

