from storage.database import get_connection


def get_choices_for_node(node_id):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                text,
                stat,
                amount,
                next_node,
                result,
                job,
                job_focus,
                artifact_granted
            FROM choices
            WHERE node_id = ?
            ORDER BY choice_order
        """, (str(node_id),))

        rows = cursor.fetchall()

    choices = [
        {
            "id": row["id"],
            "text": row["text"],
            "stat": row["stat"],
            "amount": row["amount"],
            "next": row["next_node"],
            "result": row["result"],
            "job": row["job"],
            "job_focus": row["job_focus"],
            "artifact": row["artifact_granted"]
        }
        for row in rows
    ]

    return choices


def get_node(node_id):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                type,
                title,
                text,
                next_node
            FROM nodes
            WHERE id = ?
        """, (str(node_id),))

        row = cursor.fetchone()

    if row is None:
        return None

    node = {
        "id": row["id"],
        "type": row["type"],
        "title": row["title"],
        "text": row["text"],
        "next": row["next_node"]
    }

    choices = get_choices_for_node(node_id)

    if choices:
        node["choices"] = choices

    return node


def get_artifact_result(choice_id, artifact_name):
    if not artifact_name:
        return None

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT result_text
            FROM choice_artifact_results
            WHERE choice_id = ? AND artifact_name = ?
        """, (choice_id, artifact_name))

        row = cursor.fetchone()

    if row is None:
        return None

    return row["result_text"]