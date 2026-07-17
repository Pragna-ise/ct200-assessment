from app.database.database import get_connection
from app.services.staleness_service import (
    check_staleness
)


def get_generation(generation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM generations
    WHERE id = ?
    """, (generation_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        return {
            "error": "Generation not found"
        }

    generation = dict(row)

    staleness = check_staleness(
        generation_id
    )

    generation["stale"] = (
        staleness["stale"]
    )

    generation["impact"] = (
        staleness["impact"]
    )

    return generation
def get_generations_by_selection(
    selection_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM generations
    WHERE selection_id = ?
    """, (selection_id,))

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        generation = dict(row)

        staleness = check_staleness(
            generation["id"]
        )

        generation["stale"] = (
            staleness["stale"]
        )

        generation["impact"] = (
            staleness["impact"]
        )

        results.append(
            generation
        )

    return results
def get_generations_by_node(
    node_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT g.*
    FROM generations g
    JOIN selection_nodes sn
    ON g.selection_id = sn.selection_id
    WHERE sn.node_id = ?
    """, (node_id,))

    rows = cursor.fetchall()

    conn.close()

    results = []

    for row in rows:

        generation = dict(row)

        staleness = check_staleness(
            generation["id"]
        )

        generation["stale"] = (
            staleness["stale"]
        )

        generation["impact"] = (
             staleness.get("impact", "unknown")
)
        results.append(
            generation
        )

    return results