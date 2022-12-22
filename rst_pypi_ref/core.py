"""Core module."""
from typing import List, Optional

from docutils import nodes
from docutils.parsers.rst import roles, states


def pypi_reference_role(
    role: str,
    rawtext: str,
    text: str,
    lineno: int,
    inliner: states.Inliner,
    options: Optional[dict] = None,
    content: Optional[List[str]] = None,
):
    """Parse ``pypi`` role."""
    options = roles.normalized_role_options(options)
    messages = []
    url = f"https://pypi.org/project/{text}/"
    return [nodes.reference(rawtext, text, refuri=url, **options)], messages


def bootstrap():
    roles.register_canonical_role("pypi", pypi_reference_role)
