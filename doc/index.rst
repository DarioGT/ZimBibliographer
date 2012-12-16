.. ZimBibliographer documentation master file, created by
   sphinx-quickstart on Thu Sep 27 22:21:49 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ZimBibliographer's documentation!
============================================

:Author: François Boulogne
:Download: `Stable version <http://sciunto.org/source/>`_
:Developer's corner: `github.com project <https://github.com/sciunto/ZimBibliographer>`_
:Generated: |today|
:License: GPL v3
:Version: |release|

`Zim <http://zim-wiki.org>`_ is a desktop wiki.
ZimBibliographer is a command line tool using a bibtex to add references.

In your notes, you can write keys like
  cite{Author1976}

ZimBibliographer will replace that by a link to the file (pdf, ps...)
included your bibtex you manage elsewhere.


Usage
-----

.. code-block:: sh

    zimbibliographer -h


Contents:

.. toctree::
   :maxdepth: 2


How to install
==============

Requirements
------------

* python 3
* `python-libZimSciunto <http://pypi.python.org/pypi/libZimSciunto/>`_

Install
-------

A package is available on `pypi <http://pypi.python.org/pypi/ZimBibliographer/>`_.
Otherwise, you can install it by running:

.. code-block:: sh

    python setup.py install --root='/'




Configuration
=============

The default file is ~/.zimbibliographer/bibtex.conf

It's syntax looks like:

.. code-block:: text 

    [mybiblio]
    path=~/biblio/biblio.bib
    [books]
    path=~/books/books.bib


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

