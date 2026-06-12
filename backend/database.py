import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("database_url") or os.getenv("DATABASE_URL")
USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    import psycopg2


def get_connection():
    if USE_POSTGRES:
        return psycopg2.connect(DATABASE_URL)

    db_path = os.path.join(os.path.dirname(__file__), "db.sqlite3")
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if USE_POSTGRES:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    sentiment VARCHAR(20) NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                )""")
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )""")
        conn.commit()
        print("Database ready.")
    finally:
        cursor.close()
        conn.close()


def insert_message(text: str, sentiment: str):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if USE_POSTGRES:
            cursor.execute(
                """
                INSERT INTO messages (text, sentiment)
                VALUES (%s, %s)
                RETURNING id, text, sentiment, timestamp
                """,
                (text, sentiment),
            )
            row = cursor.fetchone()
        else:
            cursor.execute(
                """
                INSERT INTO messages (text, sentiment)
                VALUES (?, ?)
                """,
                (text, sentiment),
            )
            conn.commit()
            last_id = cursor.lastrowid
            cursor.execute(
                """
                SELECT id, text, sentiment, timestamp
                FROM messages
                WHERE id = ?
                """,
                (last_id,),
            )
            row = cursor.fetchone()
        conn.commit()
        return row
    finally:
        cursor.close()
        conn.close()


def fetch_messages():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, text, sentiment, timestamp
            FROM messages
            ORDER BY timestamp DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()