#!/usr/bin/env python
"""Local work-check endpoint."""
from docutils.core import publish_cmdline

from rst_pypi_ref.core import VerifyOptions, configure

if __name__ == "__main__":
    options = VerifyOptions()
    configure(options)
    publish_cmdline()
