import sqlite3
import pandas as pd
import spacy
from src.config import DB_PATH

def extract_skills_from_text(text, skill_list):
    found = []
    for skill in skill_list:
        if skill.lower() in text.lower():
            found.append(skill)
    return list(set(found))

def main():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT rowid, * FROM jobs", conn)  # include rowid

    cur = conn.cursor()
    cur.execute("PRAGMA table_info(jobs)")
    columns = [col[1] for col in cur.fetchall()]
    if "skills" not in columns:
        cur.execute("ALTER TABLE jobs ADD COLUMN skills TEXT")
        conn.commit()

    nlp = spacy.load("en_core_web_sm")

    skill_list = [
        "Python", "SQL", "Excel", "Machine Learning", "Deep Learning", "AI",
        "TensorFlow", "PyTorch", "NLP", "Data Analysis", "Statistics",
        "Tableau", "Power BI", "AWS", "Azure", "GCP", "Java", "C++",
        "R", "Hadoop", "Spark", "Scala", "Docker", "Kubernetes"
    ]

    for idx, row in df.iterrows():
        desc = str(row.get("description", ""))
        if desc.strip():
            skills = extract_skills_from_text(desc, skill_list)
            skills_str = ",".join(skills)
            cur.execute("UPDATE jobs SET skills = ? WHERE rowid = ?", (skills_str, row["rowid"]))

    conn.commit()
    conn.close()
    print("✅ Skills extracted and saved into jobs.db")

if __name__ == "__main__":
    main()
