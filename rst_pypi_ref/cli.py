#!/usr/bin/env python
"""Local work-check endpoint."""
from docutils.core import publish_cmdline

from rst_pypi_ref.core import bootstrap

if __name__ == "__main__":
    bootstrap()
    publish_cmdline()
