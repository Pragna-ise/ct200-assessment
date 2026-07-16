from app.database.database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_nodes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        level INTEGER,
        parent TEXT
    )
    """)

    conn.commit()
    conn.close()