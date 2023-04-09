from rst_pypi_ref import core


def test_pypi_reference_role():
    nodes, messages = core.pypi_reference_role(
        "pypi", ":pypi:`docutils`", "docutils", 0, None
    )
    assert len(nodes) == 1
    node = nodes[0]
    assert node["refuri"] == "https://pypi.org/project/docutils/"


class TestForBuildPackageUrl:
    def test_name_only(self):
        url = core.build_package_url("docutils")
        assert url == "https://pypi.org/project/docutils/"

    def test_with_version(self):
        url = core.build_package_url("docutils==0.1.0")
        assert url == "https://pypi.org/project/docutils/0.1.0/"
