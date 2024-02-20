#!/usr/bin/env python
"""Local work-check endpoint."""
import argparse
import sys

from docutils.core import publish_cmdline

from rst_pypi_ref.core import VerifyOptions, configure

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument("--strict-version", action="store_true")
parser.add_argument("--ref-pypi-site", action="store_true")


if __name__ == "__main__":
    argv = []
    if "--strict-version" in sys.argv:
        sys.argv.remove("--strict-version")
        argv.append("--strict-version")
    if "--ref-pypi-site" in sys.argv:
        sys.argv.remove("--ref-pypi-site")
        argv.append("--ref-pypi-site")
    args = parser.parse_args(argv)
    options = VerifyOptions(
        strict_version=args.strict_version, ref_pypi_site=args.ref_pypi_site
    )
    configure(options)
    publish_cmdline()
