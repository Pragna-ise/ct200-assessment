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

    return compare_versions()
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