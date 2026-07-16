from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents

nodes = parse_markdown("data/ct200_manual.md")

nodes = assign_parents(nodes)

for node in nodes:
    print(
        f"Title: {node.title}"
    )
    print(
        f"Level: {node.level}"
    )
    print(
        f"Parent: {node.parent}"
    )
    print("-" * 50)