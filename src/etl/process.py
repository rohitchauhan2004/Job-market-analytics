import os
import pandas as pd
import sqlite3
from src.config import DB_PATH

def main():
    # Input & output paths
    raw_path = os.path.join("data", "jobs.csv")
    processed_dir = os.path.join("data", "processed")
    processed_path = os.path.join(processed_dir, "jobs_clean.csv")

    # Ensure processed folder exists
    os.makedirs(processed_dir, exist_ok=True)

    # Check if raw jobs.csv exists
    if not os.path.exists(raw_path):
        print("❌ jobs.csv not found. Run fetch.py first.")
        return

    # Load raw data
    df = pd.read_csv(raw_path)

    # Select expected columns if they exist
    expected_cols = [
        "title", "company", "location", "created",
        "salary_min", "salary_max", "description", "redirect_url"
    ]
    df = df[[c for c in expected_cols if c in df.columns]]

    # Save cleaned data
    df.to_csv(processed_path, index=False)

    # Extract skills
    def extract_skills(text):
        if pd.isna(text):
            return ""
        text_lower = str(text).lower()
        skills = []
        for skill in ["python", "sql", "excel", "power bi", "tableau", "aws", "azure", "machine learning"]:
            if skill in text_lower:
                skills.append(skill)
        return ", ".join(skills)

    df["skills"] = df["description"].apply(extract_skills)

    # Save job skills
    skills_path = os.path.join(processed_dir, "job_skills.csv")
    skills_df = (
        df[["title", "company", "location", "skills"]]
        .assign(skill=lambda x: x["skills"].str.split(", "))
        .explode("skill")
        .dropna()
    )
    skills_df.to_csv(skills_path, index=False)

    # Store in SQLite (optional but useful)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("jobs_clean", conn, if_exists="replace", index=False)
    skills_df.to_sql("job_skills", conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Processed jobs saved → {processed_path} & job_skills.csv")

if __name__ == "__main__":
    main()
