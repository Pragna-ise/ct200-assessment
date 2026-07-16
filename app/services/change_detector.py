from app.database.database import get_connection


def compare_versions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, content_hash
        FROM document_nodes
        WHERE version='v1'
    """)

    v1_rows = cursor.fetchall()

    cursor.execute("""
        SELECT title, content_hash
        FROM document_nodes
        WHERE version='v2'
    """)

    v2_rows = cursor.fetchall()

    conn.close()

    v1 = {
        row["title"]: row["content_hash"]
        for row in v1_rows
    }

    v2 = {
        row["title"]: row["content_hash"]
        for row in v2_rows
    }

    changes = []

    all_titles = set(v1.keys()) | set(v2.keys())

    for title in all_titles:

        if title not in v1:

            changes.append({
                "title": title,
                "change_type": "added"
            })

        elif title not in v2:

            changes.append({
                "title": title,
                "change_type": "removed"
            })

        elif v1[title] != v2[title]:

            changes.append({
                "title": title,
                "change_type": "modified"
            })

        else:

            changes.append({
                "title": title,
                "change_type": "unchanged"
            })

    return changes
def get_change_summary():

    changes = compare_versions()

    summary = {
        "added": 0,
        "removed": 0,
        "modified": 0,
        "unchanged": 0
    }

    for change in changes:

        summary[
            change["change_type"]
        ] += 1

    return summary