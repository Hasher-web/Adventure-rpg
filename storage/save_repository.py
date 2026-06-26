from storage.database import get_connection


def save_game(player, current_scenario, slot_id=1):
    if current_scenario is None:
        current_scenario = "EXIT"

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO saves (
                slot_id,
                player_name,
                knowledge,
                trust,
                influence,
                skill,
                hp_stat,
                max_hp,
                current_hp,
                job,
                job_focus,
                job_checks,
                job_success,
                job_rank,
                artifact,
                class,
                promotion_return,
                route,
                current_scenario
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            slot_id,
            player.get("name", ""),
            player.get("knowledge", 0),
            player.get("trust", 0),
            player.get("influence", 0),
            player.get("skill", 0),
            player.get("hp_stat", 0),
            player.get("max_hp", 100),
            player.get("current_hp", 100),
            player.get("job"),
            player.get("job_focus"),
            player.get("job_checks", 0),
            player.get("job_success", 0),
            player.get("job_rank", 0),
            player.get("artifact"),
            player.get("class"),
            player.get("promotion_return"),
            player.get("route"),
            current_scenario
        ))

        connection.commit()


def load_game(slot_id=1):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM saves
            WHERE slot_id = ?
        """, (slot_id,))

        row = cursor.fetchone()

    if row is None:
        return None

    player = {
        "name": row["player_name"],
        "knowledge": row["knowledge"],
        "trust": row["trust"],
        "influence": row["influence"],
        "skill": row["skill"],
        "hp_stat": row["hp_stat"],
        "max_hp": row["max_hp"],
        "current_hp": row["current_hp"],
        "job": row["job"],
        "job_focus": row["job_focus"],
        "job_checks": row["job_checks"],
        "job_success": row["job_success"],
        "job_rank": row["job_rank"],
        "artifact": row["artifact"],
        "class": row["class"],
        "promotion_return": row["promotion_return"],
        "route": row["route"]
    }

    return {
        "player": player,
        "current_scenario": row["current_scenario"]
    }