from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents


def test_parent_assignment():

    nodes = parse_markdown(
        "data/ct200_manual.md"
    )

    nodes = assign_parents(nodes)

    has_parent = False

    for node in nodes:

        if node.level > 1:

            if node.parent is not None:

                has_parent = True

    assert has_parent