from app.database.database import get_connection


def save_node(node):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO document_nodes
        (
            title,
            content,
            level,
            parent
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            node.title,
            node.content,
            node.level,
            node.parent
        )
    )

    conn.commit()
    conn.close()
def save_nodes(nodes):

    for node in nodes:
        save_node(node)