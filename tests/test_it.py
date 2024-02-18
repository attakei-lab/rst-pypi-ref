"""Test cases for core behaiviors."""
from docutils import nodes
from docutils.core import publish_doctree

from rst_pypi_ref import core


class TestForPyPiReferenceRole:
    def test_name_only(self):
        pypi_reference_role = core.pypi_reference_role(core.VerifyOptions())
        nodes, messages = pypi_reference_role(
            "pypi", ":pypi:`docutils`", "docutils", 0, None
        )
        assert len(nodes) == 1
        node = nodes[0]
        assert node["refuri"] == "https://pypi.org/project/docutils/"

    def test_title_and_target(self):
        pypi_reference_role = core.pypi_reference_role(core.VerifyOptions())
        nodes, messages = pypi_reference_role(
            "pypi", ":pypi:`PyPI Link <docutils>`", "PyPI Link <docutils>", 0, None
        )
        assert len(nodes) == 1
        node = nodes[0]
        assert node["refuri"] == "https://pypi.org/project/docutils/"


class TestForProject:
    def test_name_only(self):
        project = core.Project(name="docutils")
        assert project.url == "https://pypi.org/project/docutils/"

    def test_with_version(self):
        project = core.Project(name="docutils", version="0.1.0")
        assert project.url == "https://pypi.org/project/docutils/0.1.0/"


class TestForParse:
    def setup_method(self):
        core.bootstrap()

    def teardown_method(self):
        from docutils.parsers.rst import roles

        del roles._role_registry["pypi"]

    def test_simple_name_only(self):
        doctree: nodes.document = publish_doctree(":pypi:`docutils`")
        refs = list(doctree.findall(nodes.reference))
        assert len(refs) == 1
        assert refs[0]["refuri"] == "https://pypi.org/project/docutils/"

    def test_simple_with_version(self):
        doctree: nodes.document = publish_doctree(":pypi:`docutils==0.3`")
        refs = list(doctree.findall(nodes.reference))
        assert len(refs) == 1
        assert refs[0]["refuri"] == "https://pypi.org/project/docutils/0.3/"
