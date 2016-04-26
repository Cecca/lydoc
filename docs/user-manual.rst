###########
User Manual
###########

.. highlight:: lilypond

.. toctree::
   :maxdepth: 2


Documentation syntax
====================

Documentation of items in Lilypond documents is provided with special
comment blocks::

  %{!
  % Here goes the documentation!
  %}
  someCoolFunction =
  #(define-music-function
    (parser location music?) (mus)
      ...)

Notice that the documentation block is just a plain Lilypond block
comment, with a bang ``!`` after the opening brace. If the comment
misses the ``!``, then it is not interpreted as a documentation
comment::

  %{
  % This is just a plain comment.
  %}
  someCoolFunction =
  #(define-music-function
    (parser location music?) (mus)
      ...)

The text formatting inside the documentation comment is free, there
are no particular requirements::

  %{! This is valid %}

and::

  %{!

  This is also
             valid
  %}

Lydoc will strip the leading indentation spaces and ``%`` characters
upon reading the documentation comment. Therefore::

  %{!
  % Some complex comment:
  %
  %   - multi line
  %   - with lists
  %   - indented
  %   - with leading `%` characters
  %}

will be read like::

  Some complex comment:
  
    - multi line
    - with lists
    - indented
    - with leading `%` characters
      

Command line interface
======================

.. todo::
   write about the command line interface


Using Lydoc with Sphinx
=======================

`Sphinx`_ is an excellent documentation generator, originally created
for documenting the Python language. This short tutorial shows how to
use Lydoc along with Sphinx.

Sphinx is on the Python Package Index, so you just need to issue the
following command::

  pip instlal sphinx

which install the ``sphinx`` command line tools.

Then, you can use the ``sphinx-quickstart`` program to create a stub
for your documentation in the ``docs`` directory::

  sphinx-quickstart docs

The program asks some questions about the project.

Once you have generated the stub for the documentation of your
project, you can use Lydoc to extract the API documentation from your
Lilypond library::

  lydoc -o docs/api.rst .

The above command reads all the lilypond files in the current
directory (recursively) and outputs the API documentation in the
``docs/api.rst`` reStructuredText file.

At this point, it only remains to include ``docs/api.rst`` into your
documentation by modifying ``docs/index.rst`` as follows

.. code-block:: rest

  ###################
  Name of the project
  ###################

  .. toctree::
     :maxdepth: 2

     api

.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
