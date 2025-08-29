# src/etl/ingest.py
import json, pathlib
from sqlalchemy import create_engine, text
from src.config import DB_URL

SAMPLE = pathlib.Path("sample_data/sample_jobs.jsonl")

def main():
    engine = create_engine(DB_URL, future=True)
    with engine.begin() as conn:
        count = 0
        with open(SAMPLE, "r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                conn.execute(text("""
                    insert into jobs_raw(external_id, source, company, title, location_raw, posted_at, url, description, raw)
                    values(:external_id, :source, :company, :title, :location_raw, :posted_at, :url, :description, :raw)
                """), {
                    **row, "location_raw": row.get("location"), "raw": json.dumps(row)
                })
                count += 1
        print(f"✅ Ingested {count} raw postings")

if __name__ == "__main__":
    main()
