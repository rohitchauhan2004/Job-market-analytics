import subprocess
import sys

# Map CLI steps to your actual Python scripts
steps = {
    "fetch_jobs": "fetch_jobs",
    "process": "process",
    "export": "export",
}

def run_step(step):
    print(f"\n▶️ Running step: {step}\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    if result.returncode != 0:
        raise RuntimeError(f"❌ {step} failed!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Usage: python run_pipeline.py [fetch_jobs|process|export|dashboard|all]")
        sys.exit(1)

    step = sys.argv[1]

    if step == "all":
        for s in ["fetch_jobs", "process", "export"]:
            run_step(steps[s])
        print("✅ ETL pipeline completed successfully!")
    elif step == "dashboard":
        print("🚀 Launching Streamlit dashboard...")
        subprocess.run(["streamlit", "run", "streamlit_app.py"])
    elif step in steps:
        run_step(steps[step])
    else:
        print(f"⚠️ Unknown step: {step}")
        sys.exit(1)
