from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents
from app.services.storage_service import save_nodes

nodes = parse_markdown(
    "data/ct200_manual.md"
)

nodes = assign_parents(nodes)

save_nodes(nodes)

print("Nodes Stored Successfully")