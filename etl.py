# etl.py
import sys
import os

# Ensure src is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from etl import fetch_jobs, ingest, process, skills, export

def main():
    print("🚀 Starting ETL pipeline...")

    # 1. Fetch jobs from API/source
    print("📥 Fetching jobs...")
    jobs = fetch_jobs.run()

    # 2. Ingest raw data into database
    print("📂 Ingesting jobs into database...")
    ingest.run(jobs)

    # 3. Process jobs (cleaning, transformation)
    print("⚙️ Processing jobs...")
    processed = process.run()

    # 4. Extract skills & NLP analysis
    print("🧠 Extracting skills...")
    skills.run(processed)

    # 5. Export / finalize data
    print("💾 Exporting final dataset...")
    export.run()

    print("✅ ETL pipeline finished successfully!")

if __name__ == "__main__":
    main()
