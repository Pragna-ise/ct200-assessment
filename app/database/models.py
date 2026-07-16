from app.database.database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_nodes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        version TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        level INTEGER,
        parent TEXT,
        content_hash TEXT
    )
    """)

    conn.commit()
    conn.close()