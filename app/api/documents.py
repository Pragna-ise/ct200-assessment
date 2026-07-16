from fastapi import APIRouter
from app.services.markdown_parser import parse_markdown
from app.services.tree_builder import assign_parents

router = APIRouter()

@router.get("/parse")
def parse_document():

    nodes = parse_markdown("data/ct200_manual.md")

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