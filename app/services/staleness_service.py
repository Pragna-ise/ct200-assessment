import hashlib

from app.database.database import get_connection
def calculate_selection_hash(selection_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT n.content
    FROM nodes n
    JOIN selection_nodes sn
    ON n.id = sn.node_id
    WHERE sn.selection_id = ?
    """, (selection_id,))

    rows = cursor.fetchall()

    conn.close()

    text = ""

    for row in rows:
        text += row["content"]

    return hashlib.sha256(
        text.encode()
    ).hexdigest()
def check_staleness(generation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT selection_id,
           source_hash
    FROM generations
    WHERE id = ?
    """, (generation_id,))

    generation = cursor.fetchone()

    conn.close()

    if not generation:

        return {
            "error": "Generation not found"
        }

    current_hash = calculate_selection_hash(
        generation["selection_id"]
    )

    stale = (
        current_hash
        != generation["source_hash"]
    )

    return {
        "generation_id": generation_id,
        "stale": stale,
        "stored_hash": generation["source_hash"],
        "current_hash": current_hash
    }
