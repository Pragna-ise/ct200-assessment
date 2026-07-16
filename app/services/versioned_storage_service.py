import hashlib

from app.database.database import get_connection


def get_or_create_document(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM documents WHERE name=?",
        (name,)
    )

    row = cursor.fetchone()

    if row:
        conn.close()
        return row["id"]

    cursor.execute(
        "INSERT INTO documents(name) VALUES(?)",
        (name,)
    )

    document_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return document_id


def create_version(document_id, version_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO document_versions
        (
            document_id,
            version_name
        )
        VALUES (?,?)
        """,
        (
            document_id,
            version_name
        )
    )

    version_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return version_id


def save_nodes(nodes, version_id):

    conn = get_connection()
    cursor = conn.cursor()

    for node in nodes:

        content_hash = hashlib.sha256(
            node.content.encode()
        ).hexdigest()

        logical_node_id = node.title.lower()

        cursor.execute(
            """
            INSERT INTO nodes
            (
                logical_node_id,
                version_id,
                title,
                content,
                content_hash,
                level,
                parent_title
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                logical_node_id,
                version_id,
                node.title,
                node.content,
                content_hash,
                node.level,
                node.parent
            )
        )

    conn.commit()
    conn.close()