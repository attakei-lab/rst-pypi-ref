"""Sphinx extension handler module."""
from sphinx.application import Sphinx
from sphinx.config import Config

from . import __version__
from .core import VerifyOptions, configure


def register_roles(app: Sphinx, config: Config):
    options = VerifyOptions()
    configure(options)


def setup(app: Sphinx):
    app.connect("config-inited", register_roles)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": False,
    }
