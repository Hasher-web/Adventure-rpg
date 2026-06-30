import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "game.db"
NODES_JSON_PATH = DATA_DIR / "nodes.json"
SAVE_JSON_PATH = DATA_DIR / "save.json"

print("[BASE_DIR]", BASE_DIR)
print("[DATA_DIR]", DATA_DIR)
print("[DB_PATH]", DB_PATH)
print("[NODES_JSON_PATH EXISTS]", NODES_JSON_PATH.exists())
print("[SAVE_JSON_PATH EXISTS]", SAVE_JSON_PATH.exists())

DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                next_node TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                choice_order INTEGER NOT NULL,
                text TEXT NOT NULL,
                next_node TEXT,
                stat TEXT,
                amount INTEGER DEFAULT 0,
                result TEXT,
                job TEXT,
                job_focus TEXT,
                artifact_granted TEXT,
                FOREIGN KEY (node_id) REFERENCES nodes(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS choice_artifact_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                choice_id INTEGER NOT NULL,
                artifact_name TEXT NOT NULL,
                result_text TEXT NOT NULL,
                FOREIGN KEY (choice_id) REFERENCES choices(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS choice_next_artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                choice_id INTEGER NOT NULL,
                artifact_name TEXT NOT NULL,
                next_node TEXT NOT NULL,
                FOREIGN KEY (choice_id) REFERENCES choices(id),
                UNIQUE(choice_id, artifact_name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saves (
                slot_id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                knowledge INTEGER NOT NULL DEFAULT 0,
                trust INTEGER NOT NULL DEFAULT 0,
                influence INTEGER NOT NULL DEFAULT 0,
                skill INTEGER NOT NULL DEFAULT 0,
                hp_stat INTEGER NOT NULL DEFAULT 0,
                max_hp INTEGER NOT NULL DEFAULT 100,
                current_hp INTEGER NOT NULL DEFAULT 100,
                job TEXT,
                job_focus TEXT,
                job_checks INTEGER NOT NULL DEFAULT 0,
                job_success INTEGER NOT NULL DEFAULT 0,
                job_rank INTEGER NOT NULL DEFAULT 0,
                artifact TEXT,
                class TEXT,
                promotion_return TEXT,
                route TEXT,
                current_scenario TEXT NOT NULL
            )
        """)

        connection.commit()


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def clear_existing_data(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM choice_artifact_results")
    cursor.execute("DELETE FROM choices")
    cursor.execute("DELETE FROM saves")
    cursor.execute("DELETE FROM nodes")
    connection.commit()


def migrate_nodes(connection, nodes_data):
    cursor = connection.cursor()

    imported_nodes = 0
    imported_choices = 0
    imported_artifact_results = 0

    for node_id, node in nodes_data.items():
        node_type = node.get("type")
        title = node.get("title", "")
        text = node.get("text", "")
        next_node = node.get("next")

        cursor.execute("""
            INSERT INTO nodes (id, type, title, text, next_node)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(node_id),
            node_type,
            title,
            text,
            next_node
        ))
        imported_nodes += 1

        choices = node.get("choices", [])

        for choice_index, choice in enumerate(choices, start=1):
            choice_text = choice.get("text", "")
            choice_next = choice.get("next")
            stat = choice.get("stat")
            amount = choice.get("amount", 0)
            result = choice.get("result")
            job = choice.get("job")
            job_focus = choice.get("job_focus")
            artifact_granted = choice.get("artifact")

            cursor.execute("""
                INSERT INTO choices (
                    node_id,
                    choice_order,
                    text,
                    next_node,
                    stat,
                    amount,
                    result,
                    job,
                    job_focus,
                    artifact_granted
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(node_id),
                choice_index,
                choice_text,
                choice_next,
                stat,
                amount,
                result,
                job,
                job_focus,
                artifact_granted
            ))
            imported_choices += 1

            choice_id = cursor.lastrowid

            artifact_results = choice.get("artifact_result", {})
            for artifact_name, result_text in artifact_results.items():
                cursor.execute("""
                    INSERT INTO choice_artifact_results (
                        choice_id,
                        artifact_name,
                        result_text
                    )
                    VALUES (?, ?, ?)
                """, (
                    choice_id,
                    artifact_name,
                    result_text
                ))
                imported_artifact_results += 1

    connection.commit()

    print("[IMPORTED NODES]", imported_nodes)
    print("[IMPORTED CHOICES]", imported_choices)
    print("[IMPORTED ARTIFACT RESULTS]", imported_artifact_results)


def migrate_save(connection, save_data):
    if not save_data:
        print("[SAVE] No save.json found, skipping save migration")
        return

    player = save_data.get("player")
    current_scenario = save_data.get("current_scenario")

    if not player or current_scenario is None:
        print("[SAVE] save.json missing player or current_scenario, skipping")
        return

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO saves (
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
        1,
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
    print("[SAVE] Migrated save slot 1")


def debug_database(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM nodes")
    print("[DB NODE COUNT]", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM choices")
    print("[DB CHOICE COUNT]", cursor.fetchone()[0])

    cursor.execute("SELECT id FROM nodes ORDER BY id LIMIT 20")
    rows = cursor.fetchall()
    print("[FIRST 20 NODE IDS]", [row[0] for row in rows])

    cursor.execute("SELECT id, title FROM nodes WHERE id = '1'")
    row = cursor.fetchone()
    print("[NODE 1 EXISTS]", dict(row) if row else None)


def main():
    initialize_database()

    nodes_data = load_json(NODES_JSON_PATH)
    save_data = load_json(SAVE_JSON_PATH) if SAVE_JSON_PATH.exists() else None

    with get_connection() as connection:
        clear_existing_data(connection)
        migrate_nodes(connection, nodes_data)
        migrate_save(connection, save_data)
        debug_database(connection)

    print("Migration complete.")


if __name__ == "__main__":
    main()