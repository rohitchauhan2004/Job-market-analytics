# run_etl.py
from src.etl import fetch_jobs, ingest, process, skills, export

def run_etl():
    print("🚀 Starting ETL pipeline...")
    try:
        # 1. Fetch jobs
        fetch_jobs.main()

        # 2. Ingest raw jobs into database
        ingest.main()

        # 3. Process data (cleaning, transformations)
        process.main()

        # 4. Extract skills (NLP)
        skills.main()

        # 5. Export cleaned data
        export.main()

        print("✅ ETL pipeline completed successfully!")

    except Exception as e:
        print(f"❌ ETL pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_etl()
