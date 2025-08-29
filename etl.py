import sys
import os

# Make sure src/ is on Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from etl import fetch_jobs, ingest, process, skills, export

def run_etl():
    print("🚀 Starting ETL pipeline...")

    try:
        jobs = fetch_jobs.fetch_job_listings()
        print(f"✅ Fetched {len(jobs)} jobs")

        df = ingest.ingest_data(jobs)
        print("✅ Ingested data")

        processed_df = process.clean_data(df)
        print("✅ Processed data")

        skill_stats = skills.extract_skills(processed_df)
        print("✅ Extracted skills")

        export.export_to_sqlite(processed_df, "jobs.db")
        print("✅ Exported to jobs.db")

        print("🎉 ETL pipeline completed successfully!")

    except Exception as e:
        print(f"❌ ETL pipeline failed: {e}")


if __name__ == "__main__":
    run_etl()
