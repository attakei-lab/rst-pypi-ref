"""Test cases for sphinx."""
import pytest
from sphinx.testing.util import SphinxTestApp

from rst_pypi_ref.core import VerifyOptions


@pytest.mark.sphinx("html", testroot="default")
def test_work_on_sphinx(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()


@pytest.mark.sphinx(
    "html", testroot="default", confoverrides={"rst_pypi_ref_options": {}}
)
def test_work_with_empty_options(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()


@pytest.mark.sphinx(
    "html",
    testroot="default",
    confoverrides={"rst_pypi_ref_options": {"strict_version": True}},
)
def test_work_with_strict_version(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()


@pytest.mark.sphinx(
    "html",
    testroot="default",
    confoverrides={"rst_pypi_ref_options": {"ref_pypi_site": True}},
)
def test_work_with_ref_pypi_site(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()


@pytest.mark.sphinx(
    "html",
    testroot="default",
    confoverrides={"rst_pypi_ref_options": {"ref_pypi_site": VerifyOptions()}},
)
def test_work_with_instance(app: SphinxTestApp):
    app.build()
    index_html = app.outdir / "index.html"
    assert index_html.exists()
    assert "https://pypi.org/project/sphinx-revealjs/" in index_html.read_text()
