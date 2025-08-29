import sqlite3
import pandas as pd
from src.config import DB_PATH

def extract_skills(text):
    if pd.isna(text):
        return ""
    text_lower = str(text).lower()
    skills = []
    for skill in ["python", "sql", "excel", "power bi", "tableau", "aws", "azure", "machine learning"]:
        if skill in text_lower:
            skills.append(skill)
    return ", ".join(skills)

def run_nlp_skill_extraction():
    conn = sqlite3.connect(DB_PATH)

    # Load job descriptions (no id in table, so we create one)
    df = pd.read_sql("SELECT description FROM jobs", conn)
    df = df.reset_index().rename(columns={"index": "id"})  # synthetic ID

    # Extract skills
    df["skills"] = df["description"].apply(extract_skills)

    # Save into job_skills_nlp
    df[["id", "skills"]].to_sql("job_skills_nlp", conn, if_exists="replace", index=False)

    conn.close()
    print("✅ NLP skills extracted and saved to job_skills_nlp")

if __name__ == "__main__":
    run_nlp_skill_extraction()
