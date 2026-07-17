from fastapi import APIRouter

from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents
from app.services.ingestion_service import ingest_document
from app.database.database import get_connection
from app.services.change_detector import compare_versions
from app.services.change_detector import (
    compare_versions,
    get_change_summary
)
from app.services.browse_service import get_top_sections
from app.services.browse_service import get_node
from app.services.browse_service import search_nodes
from app.services.browse_service import node_changes
from app.services.generation_service import (
    generate_test_cases
)
from app.services.staleness_service import (
    check_staleness
)
from app.services.retrieval_service import (
    get_generation,
    get_generations_by_selection,
    get_generations_by_node
)
router = APIRouter()


@router.get("/parse")
def parse_document():

    nodes = parse_markdown(
        "data/ct200_manual.md"
    )

    nodes = assign_parents(nodes)

    return [
        {
            "title": node.title,
            "level": node.level,
            "parent": node.parent,
            "content": node.content
        }
        for node in nodes
    ]


@router.get("/nodes")
def get_nodes():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM document_nodes"
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.post("/ingest/v1")
def ingest_v1():

    count = ingest_document(
        "data/ct200_manual.md",
        "v1"
    )

    return {
        "message": "Version 1 ingested",
        "nodes_stored": count
    }


@router.post("/ingest/v2")
def ingest_v2():

    count = ingest_document(
        "data/ct200_manual_v2.md",
        "v2"
    )

    return {
        "message": "Version 2 ingested",
        "nodes_stored": count
    }
@router.get("/compare")

def compare_documents():

    changes = compare_versions()

    return {
        "total_changes": len(changes),
        "results": changes
    }
@router.get("/compare")
def compare_documents():

    changes = compare_versions()

    return {
        "total_changes": len(changes),
        "results": changes
    }
@router.get("/compare/summary")
def compare_summary():

    return get_change_summary()
@router.get("/sections")
def sections(version: str = "v2"):
    return get_top_sections(version)
@router.get("/node/{node_id}")
def node(node_id: int):
    return get_node(node_id)
@router.get("/search")
def search(q: str):

    return search_nodes(q)
@router.get("/changes/{logical_node_id}")
def changes(logical_node_id: str):

    return node_changes(
        logical_node_id
    )
@router.post("/generate/{selection_id}")
def generate(
    selection_id: int
):

    return generate_test_cases(
        selection_id
    )
@router.get(
    "/generation/{generation_id}/staleness"
)
def generation_staleness(
    generation_id: int
):

    return check_staleness(
        generation_id
    )
def get_impact_level(
    old_hash,
    new_hash
):

    if old_hash == new_hash:

        return "none"

    return "unknown"
    return {
    "generation_id": generation_id,
    "stale": stale,
    "impact": (
        "unknown"
        if stale
        else "none"
    )
}
@router.get(
    "/generations/{generation_id}"
)
def generation(
    generation_id: int
):

    return get_generation(
        generation_id
    )
@router.get(
    "/selection/{selection_id}/generations"
)
def selection_generations(
    selection_id: int
):

    return get_generations_by_selection(
        selection_id
    )
@router.get(
    "/node/{node_id}/generations"
)
def node_generations(
    node_id: int
):

    return get_generations_by_node(
        node_id
    )