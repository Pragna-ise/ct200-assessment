from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents
from app.services.storage_service import save_nodes


def ingest_document(file_path, version):

    nodes = parse_markdown(file_path)

    nodes = assign_parents(nodes)

    save_nodes(nodes, version)

    return len(nodes)