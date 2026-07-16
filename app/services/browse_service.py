from app.database.database import get_connection

def get_top_sections(version_name="v2"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT n.id,n.title,n.level
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
            "changed": False,
            "message": "Only one version exists"
        }

    changed = (
        rows[0]["content_hash"]
        != rows[-1]["content_hash"]
    )

    return {
        "logical_node_id": logical_node_id,
        "changed": changed
    }