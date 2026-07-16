from app.database.database import get_connection


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # Document Versions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_versions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        version_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(document_id) REFERENCES documents(id)
    )
    """)

    # Nodes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nodes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        logical_node_id TEXT,
        version_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        content_hash TEXT,
        level INTEGER,
        parent_title TEXT,
        FOREIGN KEY(version_id) REFERENCES document_versions(id)
    )
    """)

    # Selections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS selections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Selection Nodes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS selection_nodes(
        selection_id INTEGER,
        node_id INTEGER,
        PRIMARY KEY(selection_id, node_id),
        FOREIGN KEY(selection_id) REFERENCES selections(id),
        FOREIGN KEY(node_id) REFERENCES nodes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        selection_id INTEGER,
        generated_text TEXT,
        model_name TEXT,
        source_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(selection_id) REFERENCES selections(id)
    )
    """)

    conn.commit()
    conn.close()