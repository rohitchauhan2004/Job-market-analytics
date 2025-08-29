import os
import sqlite3
import pandas as pd
from src.config import DB_PATH

def main():
    # Load processed data
    processed_path = os.path.join("data", "processed", "jobs_clean.csv")
    if not os.path.exists(processed_path):
        print("❌ Processed file not found. Run process.py first.")
        return

    df = pd.read_csv(processed_path)

    # Keep only expected columns
    expected_cols = [
        "title",
        "company",
        "location",
        "created",
        "salary_min",
        "salary_max",
        "description",
        "redirect_url"
    ]
    df = df[[c for c in expected_cols if c in df.columns]]

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table (with id column)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        created TEXT,
        salary_min REAL,
        salary_max REAL,
        description TEXT,
        redirect_url TEXT
    );
    """)

    # Clear old data
    cursor.execute("DELETE FROM jobs")

    # Insert new data
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO jobs (title, company, location, created, salary_min, salary_max, description, redirect_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("title"),
            row.get("company"),
            row.get("location"),
            row.get("created"),
            row.get("salary_min"),
            row.get("salary_max"),
            row.get("description"),
            row.get("redirect_url")
        ))

    conn.commit()
    conn.close()
    print("✅ Data exported to jobs.db (table: jobs)")

if __name__ == "__main__":
    main()
