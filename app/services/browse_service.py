from app.database.database import get_connection


def get_top_sections(version_name="v2"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT n.id,
               n.title,
               n.level
        FROM nodes n
        JOIN document_versions dv
        ON n.version_id = dv.id
        WHERE dv.version_name = ?
        AND n.level = 2
    """, (version_name,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_node(node_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM nodes WHERE id=?",
        (node_id,)
    )

    node = cursor.fetchone()

    if not node:

        conn.close()

        return {
            "error": "Node not found"
        }

    cursor.execute(
        """
        SELECT *
        FROM nodes
        WHERE parent_title=?
        """,
        (node["title"],)
    )

    children = cursor.fetchall()

    conn.close()

    return {
        "node": dict(node),
        "children": [
            dict(child)
            for child in children
        ]
    }


def search_nodes(query):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM nodes
        WHERE title LIKE ?
        OR content LIKE ?
        """,
        (
            f"%{query}%",
            f"%{query}%"
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def node_changes(logical_node_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT version_id,
               title,
               content_hash
        FROM nodes
        WHERE logical_node_id=?
        ORDER BY version_id
        """,
        (logical_node_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    if len(rows) < 2:

        return {
            "logical_node_id": logical_node_id,
            "changed": False,
            "summary": "Only one version exists",
            "versions_found": len(rows)
        }

    old_hash = rows[0]["content_hash"]
    new_hash = rows[-1]["content_hash"]

    changed = old_hash != new_hash

    if changed:

        summary = (
            f"Content changed between "
            f"version {rows[0]['version_id']} "
            f"and version {rows[-1]['version_id']}"
        )

    else:

        summary = (
            "No content change detected"
        )

    return {
        "logical_node_id": logical_node_id,
        "changed": changed,
        "summary": summary,
        "versions_found": len(rows)
    }