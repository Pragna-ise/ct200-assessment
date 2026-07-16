import hashlib

from app.database.database import get_connection


def save_node(node, version):

    conn = get_connection()

    cursor = conn.cursor()

    content_hash = hashlib.sha256(
        node.content.encode()
    ).hexdigest()

    cursor.execute(
        """
        INSERT INTO document_nodes
        (
            version,
            title,
            content,
            level,
            parent,
            content_hash
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            version,
            node.title,
            node.content,
            node.level,
            node.parent,
            content_hash
        )
    )

    conn.commit()
    conn.close()


def save_nodes(nodes, version):

    for node in nodes:
        save_node(node, version)