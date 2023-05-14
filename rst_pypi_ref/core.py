"""Core module."""
import re
from typing import List, Optional

from docutils import nodes
from docutils.parsers.rst import roles
from docutils.parsers.rst.states import Inliner


def build_package_url(fullname: str) -> str:
    """Build ref URL for package fullname after parsed."""
    spec = fullname.split("==")
    name = spec[0]
    url = f"https://pypi.org/project/{name}/"
    if len(spec) > 1:
        url += f"{spec[1]}/"
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
    url = build_package_url(target)
    return [nodes.reference(rawtext, title, refuri=url, **options)], messages


def bootstrap():
    roles.register_canonical_role("pypi", pypi_reference_role)
