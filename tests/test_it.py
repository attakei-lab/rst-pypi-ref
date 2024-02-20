"""Test cases for core behaiviors."""
import subprocess

import pytest
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

    @pytest.mark.parametrize(
        "name,version,verify_options,result_len",
        [
            ("docutils", None, core.VerifyOptions(), 0),
            ("docutils", None, core.VerifyOptions(strict_version=True), 0),
            ("docutils", None, core.VerifyOptions(ref_pypi_site=True), 0),
            ("docutils", None, core.VerifyOptions(True, True), 0),
            ("docutils", "0.3", core.VerifyOptions(), 0),
            ("docutils", "0.3", core.VerifyOptions(strict_version=True), 0),
            ("docutils", "0.3", core.VerifyOptions(ref_pypi_site=True), 0),
            ("docutils", "0.3", core.VerifyOptions(True, True), 0),
            ("docutils", "invalid", core.VerifyOptions(), 0),
            ("docutils", "invalid", core.VerifyOptions(strict_version=True), 1),
            ("docutils", "invalid", core.VerifyOptions(ref_pypi_site=True), 1),
            ("docutils", "invalid", core.VerifyOptions(True, True), 2),
            ("z", None, core.VerifyOptions(), 0),
            ("z", None, core.VerifyOptions(strict_version=True), 0),
            ("z", None, core.VerifyOptions(ref_pypi_site=True), 1),
            ("z", None, core.VerifyOptions(True, True), 1),
            ("z", "0.1", core.VerifyOptions(), 0),
            ("z", "0.1", core.VerifyOptions(strict_version=True), 0),
            ("z", "0.1", core.VerifyOptions(ref_pypi_site=True), 1),
            ("z", "0.1", core.VerifyOptions(True, True), 1),
            ("z", "invalid", core.VerifyOptions(), 0),
            ("z", "invalid", core.VerifyOptions(strict_version=True), 1),
            ("z", "invalid", core.VerifyOptions(ref_pypi_site=True), 1),
            ("z", "invalid", core.VerifyOptions(True, True), 2),
        ],
    )
    def test_verify(self, name, version, verify_options, result_len):
        project = core.Project(name=name, version=version)
        messages = project.verify(verify_options)
        assert len(messages) == result_len


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


class TestForInvalidRoleByCli:
    """Test cases for invalid source pattern."""

    def test_ref_pypi_site(self):
        """CLI I/O test for --ref-pypi-site"""
        source = ":pypi:`z`"
        expected = (
            "\n".join(
                [
                    # "<stdin>:1: (WARNING/2) 'z' is not found in PyPI.",
                    '<document source="<stdin>">',
                    "    <paragraph>",
                    '        <problematic ids="problematic-1" refid="system-message-1">',  # noqa
                    "            :pypi:`z`",
                    '    <system_message backrefs="problematic-1" ids="system-message-1" level="2" line="1" source="<stdin>" type="WARNING">',  # noqa
                    "        <paragraph>",
                    "            'z' is not found in PyPI.",
                ]
            )
            + "\n"
        )
        proc = subprocess.run(
            ["python", "-m", "rst_pypi_ref.cli", "--ref-pypi-site"],
            input=source.encode(),
            stdout=subprocess.PIPE,
        )
        assert proc.returncode == 0
        assert proc.stdout == expected.encode()
