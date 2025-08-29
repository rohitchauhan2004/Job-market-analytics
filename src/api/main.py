from fastapi import FastAPI
import pandas as pd
from pathlib import Path

app = FastAPI(title="Job Market Analytics API")

DATA_PATH = Path("data/jobs.csv")

@app.get("/")
def root():
    return {"message": "Job Market Analytics API is running 🚀"}

@app.get("/jobs")
def get_jobs(limit: int = 20):
    """Return job listings"""
    df = pd.read_csv(DATA_PATH)
    return df.head(limit).to_dict(orient="records")

@app.get("/skills")
def get_skills():
    """Return top skills from job postings"""
    df = pd.read_csv(DATA_PATH)
    if "tags" not in df.columns:
        return {"error": "No tags column found"}
    
    skills = df["tags"].dropna().str.split(",")
    all_skills = [s.strip() for sub in skills for s in sub]
    skill_counts = pd.Series(all_skills).value_counts().head(20)
    return skill_counts.to_dict()
