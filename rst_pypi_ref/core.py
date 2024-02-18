"""Core module."""
import re
from dataclasses import dataclass
from typing import List, Optional

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


def pypi_reference_role(
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
    return [nodes.reference(rawtext, title, refuri=project.url, **options)], messages


def bootstrap():
    roles.register_canonical_role("pypi", pypi_reference_role)
