from app.database.database import get_connection


def test_versions_exist():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        as count
        FROM document_versions
        """
    )

    count = cursor.fetchone()["count"]

    conn.close()

    assert count >= 2