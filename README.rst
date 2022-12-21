============
rst-pypi-ref
============

reStructuredText custom role to refer PyPI packages.

Description
===========

This is python package to provide features to refer to PyPI in docutils (and more).

Included features:

* reStructuredText role
* Sphinx extension

Installation
============

.. code-block:: console

   pip install rst-pypi-ref

Usage
=====

Simple usage
------------

.. code-block:: console

   $ echo ':pypi:`rst-pypi-ref`' | python -m rst_pypi_ref.cli
   <document source="<stdin>">
       <paragraph>
           <reference refuri="https://pypi.org/project/rst-pypi-ref">
               rst-pypi-ref

With Sphinx
-----------

.. code-block:: python

   extensions = [
       "rst_pypi_ref.sphinx",
   ]
