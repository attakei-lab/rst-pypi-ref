======================
Guide for contributing
======================

You can contribute this project by some methods.

Use this
========

If you have interested, please use it at your documentation.
And, please announce that you are using it if you can.

Reporting
=========

If you find out troubles about this or idea for enhancement, please post into `GitHub Issues <https://github.com/attakei-lab/rst-pypi-ref/issues>`_.
When you can implement about issues, please post as `pull-request <https://github.com/attakei-lab/rst-pypi-ref/pulls>`_.

About local environment
=======================

``rst-pypi-ref`` uses these for project management.

* Rye: For dependencies management
* pre-commit: For lintings.

Install Rye and pre-commit before setting up local environment.

.. rst:: console

   git clone REPO
   cd REPO
   rye sync --dev --no-lock
   rye run pytest
   pre-commit install
