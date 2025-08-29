import sys
import subprocess
import importlib

def run_etl(job_role="data analyst"):
    print(f"🚀 Running ETL pipeline for role: '{job_role}' ...")
    # Pass job_role into fetch_jobs.main(job_role)
    fetch_module = importlib.import_module("src.etl.fetch_jobs")
    fetch_module.main(job_role)

    # Ingest + Process remain same
    importlib.import_module("src.etl.ingest").main()
    importlib.import_module("src.etl.process").main()

    print("✅ ETL pipeline finished successfully!")

def run_report():
    print("🚀 Generating report...")
    module = importlib.import_module("src.analysis.report")
    module.main()
    print("✅ Report generated successfully!")

def run_dashboard():
    print("🚀 Launching Streamlit dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dash/app.py"])

def run_all(job_role="data analyst"):
    run_etl(job_role)
    run_report()
    run_dashboard()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py [etl|report|dashboard|all] [job_role]")
        sys.exit(1)

    option = sys.argv[1].lower()
    job_role = sys.argv[2] if len(sys.argv) > 2 else "data analyst"

    if option == "etl":
        run_etl(job_role)
    elif option == "report":
        run_report()
    elif option == "dashboard":
        run_dashboard()
    elif option == "all":
        run_all(job_role)
    else:
        print("❌ Invalid option. Use 'etl', 'report', 'dashboard', or 'all'.")
