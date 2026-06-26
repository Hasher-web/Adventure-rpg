from pathlib import Path
import sqlite3


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "game.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL CHECK (type IN ('scenario', 'event', 'ending')),
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
                next_node TEXT NOT NULL,
                stat TEXT,
                amount INTEGER DEFAULT 0,
                result TEXT,
                job TEXT,
                job_focus TEXT,
                artifact_granted TEXT,
                FOREIGN KEY (node_id) REFERENCES nodes(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS choice_artifact_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                choice_id INTEGER NOT NULL,
                artifact_name TEXT NOT NULL,
                result_text TEXT NOT NULL,
                FOREIGN KEY (choice_id) REFERENCES choices(id) ON DELETE CASCADE,
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