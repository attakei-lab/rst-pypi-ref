"""Sphinx extension handler module."""
from sphinx.application import Sphinx
from sphinx.config import Config

from . import __version__
from .core import VerifyOptions, configure


def register_roles(app: Sphinx, config: Config):
    options = config.rst_pypi_ref_options
    if options is None:
        options = VerifyOptions()
    elif isinstance(options, VerifyOptions):
        pass
    elif isinstance(options, dict):
        strict_version = bool(options.get("strict_version", False))
        ref_pypi_site = bool(options.get("ref_pypi_site", False))
        options = VerifyOptions(
            strict_version=strict_version, ref_pypi_site=ref_pypi_site
        )
    configure(options)


def setup(app: Sphinx):
    app.connect("config-inited", register_roles)
    app.add_config_value("rst_pypi_ref_options", None, "env", [dict, VerifyOptions])
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": False,
    }
