# src/etl/ingest.py
import json
import pathlib
from sqlalchemy import create_engine, text
from src.config import DB_URL

# Sample file path
SAMPLE = pathlib.Path("sample_data/sample_jobs.jsonl")

def main():
    engine = create_engine(DB_URL, future=True)

    with engine.begin() as conn:
        # ✅ Ensure jobs_raw table exists
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS jobs_raw (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT,
                source TEXT,
                company TEXT,
                title TEXT,
                location_raw TEXT,
                posted_at TEXT,
                url TEXT,
                description TEXT,
                raw TEXT
            )
        """))

        count = 0

        # ✅ Ingest from sample file if it exists
        if SAMPLE.exists():
            with open(SAMPLE, "r", encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    conn.execute(text("""
                        INSERT INTO jobs_raw (
                            external_id, source, company, title, location_raw,
                            posted_at, url, description, raw
                        ) VALUES (
                            :external_id, :source, :company, :title, :location_raw,
                            :posted_at, :url, :description, :raw
                        )
                    """), {
                        **row,
                        "location_raw": row.get("location"),
                        "raw": json.dumps(row)
                    })
                    count += 1
            print(f"✅ Ingested {count} raw postings")
        else:
            print(f"⚠️ Sample file not found at: {SAMPLE}")

if __name__ == "__main__":
    main()
