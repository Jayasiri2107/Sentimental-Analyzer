import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    return psycopg2.connect(os.getenv("database_url"))
def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id  SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                sentiment VARCHAR(20) NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            )""")
        conn.commit()
        print("Database ready.")
    finally:
        cursor.close()
        conn.close()