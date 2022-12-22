from rst_pypi_ref import core


def test_pypi_reference_role():
    nodes, messages = core.pypi_reference_role(
        "pypi", ":pypi:`docutils`", "docutils", 0, None
    )
    assert len(nodes) == 1
    node = nodes[0]
    assert node["refuri"] == "https://pypi.org/project/docutils/"
