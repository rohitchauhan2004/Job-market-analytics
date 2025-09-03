# run_pipeline.py
import subprocess
import sys
from run_etl import run_etl  # Import the helper we defined in run_etl.py


def run_dashboard():
    """Launch Streamlit dashboard"""
    print("\n🚀 Launching Streamlit dashboard...\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Usage: python run_pipeline.py [etl|dashboard|all]")
        sys.exit(1)

    step = sys.argv[1]

    if step == "etl":
        run_etl()

    elif step == "dashboard":
        run_dashboard()

    elif step == "all":
        print("\n▶️ Running ETL pipeline...\n")
        run_etl()
        print("\n✅ ETL pipeline completed successfully!\n")
        run_dashboard()

    else:
        print(f"⚠️ Unknown step: {step}")
        sys.exit(1)
