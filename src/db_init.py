# src/db_init.py
import sqlite3

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            date_posted TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized with 'jobs' table")

if __name__ == "__main__":
    init_db()
