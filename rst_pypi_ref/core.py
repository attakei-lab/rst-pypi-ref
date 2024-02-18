"""Core module."""
import importlib
import re
import warnings
from dataclasses import dataclass
from typing import List, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from docutils import nodes
from docutils.parsers.rst import roles
from docutils.parsers.rst.states import Inliner


@dataclass
class Project:
    """Project data struct on PyPI."""

    name: str
    version: Optional[str] = None

    @classmethod
    def parse(cls, fullname: str) -> "Project":
        spec = fullname.split("==")
        if len(spec) == 1:
            return cls(name=spec[0])
        return cls(name=spec[0], version=spec[1])

    @property
    def url(self) -> str:
        url = f"https://pypi.org/project/{self.name}/"
        if self.version:
            url += f"{self.version}/"
        return url

    def verify(self, options: "VerifyOptions") -> List[str]:
        result = []
        if options.strict_version and self.version:
            from packaging.version import InvalidVersion, Version

            try:
                Version(self.version)
            except InvalidVersion:
                result.append(f"'{self}' includes invalid version text.")
        if options.ref_pypi_site:
            try:
                msg = f"'{self}' is not found in PyPI."
                resp = urlopen(Request(self.url, method="HEAD"))
                if resp.status != 200:
                    result.append(msg)
            except HTTPError:
                result.append(msg)
        return result


@dataclass
class VerifyOptions:
    strict_version: bool = False
    """Strict verify version text by packaging."""
    ref_pypi_site: bool = False
    """Strict verify from PyPI site (check if exists)."""


def pypi_reference_role(verify_options: VerifyOptions) -> callable:
    if verify_options.strict_version:
        try:
            importlib.import_module("packaging")
        except ImportError:
            warnings.warn(
                "When use strict_version options, require `packaging`."
                "Please run `pip install 'rst-pypi-ref[strict]'"
            )

    def _pypi_reference_role(
        role: str,
        rawtext: str,
        text: str,
        lineno: int,
        inliner: Inliner,
        options: Optional[dict] = None,
        content: Optional[List[str]] = None,
    ):
        """Parse ``pypi`` role."""
        options = roles.normalized_role_options(options)
        messages = []
        title = target = text
        matched = re.match(r"^(?P<title>.+) <(?P<target>.+)>$", text)
        if matched:
            title = matched.group("title")
            target = matched.group("target")
        project = Project.parse(target)
        messages = project.verify(verify_options)
        for msg in messages:
            warnings.warn(msg)
        return [
            nodes.reference(rawtext, title, refuri=project.url, **options)
        ], messages

    return _pypi_reference_role


def configure(options: VerifyOptions):
    roles.register_canonical_role("pypi", pypi_reference_role(options))


def bootstrap():
    warnings.warn(
        "`rst_pypi_ref.core.bootstrap` is deprecated."
        "Use `rst_pypi_ref.core.configure` istead of it."
    )
    configure(VerifyOptions())
