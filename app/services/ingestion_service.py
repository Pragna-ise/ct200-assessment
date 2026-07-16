from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents

from app.services.versioned_storage_service import (
    get_or_create_document,
    create_version,
    save_nodes
)


def ingest_document(
    file_path,
    version_name
):

    nodes = parse_markdown(file_path)

    nodes = assign_parents(nodes)

    document_id = get_or_create_document(
        "CT200 Manual"
    )

    version_id = create_version(
        document_id,
        version_name
    )

    save_nodes(
        nodes,
        version_id
    )

    return len(nodes)