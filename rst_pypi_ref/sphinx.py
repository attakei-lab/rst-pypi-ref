"""Sphinx extension handler module."""
from docutils.parsers.rst import roles
from sphinx.application import Sphinx

from . import __version__
from .core import pypi_reference_role


def setup(app: Sphinx):
    roles.register_canonical_role("pypi", pypi_reference_role)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": False,
    }
