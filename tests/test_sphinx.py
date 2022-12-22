"""Test cases for sphinx."""
import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html", testroot="default")
def test_work_on_sphinx(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()
