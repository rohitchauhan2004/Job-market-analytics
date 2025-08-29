# src/analysis/report.py
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

DB_PATH = "data/jobs.db"
REPORT_PATH = "reports/job_market_report.pdf"

def generate_report():
    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)

    # 1. Query top skills
    conn = sqlite3.connect(DB_PATH)

    skills = pd.read_sql("""
        SELECT s.name AS skill, COUNT(*) AS demand
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.id
        GROUP BY s.name
        ORDER BY demand DESC
        LIMIT 10;
    """, conn)

    titles = pd.read_sql("""
        SELECT title_normalized AS title, COUNT(*) AS demand
        FROM jobs_clean
        GROUP BY title_normalized
        ORDER BY demand DESC
        LIMIT 10;
    """, conn)

    conn.close()

    # 2. Generate plots
    plt.figure(figsize=(8,5))
    skills.plot(kind="barh", x="skill", y="demand", legend=False)
    plt.gca().invert_yaxis()
    plt.title("Top 10 Skills in Demand")
    plt.xlabel("Job Postings")
    plt.tight_layout()
    plt.savefig("reports/top_skills.png")

    plt.figure(figsize=(8,5))
    titles.plot(kind="barh", x="title", y="demand", legend=False)
    plt.gca().invert_yaxis()
    plt.title("Top 10 Job Titles")
    plt.xlabel("Job Postings")
    plt.tight_layout()
    plt.savefig("reports/top_titles.png")

    # 3. Build PDF
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(REPORT_PATH, pagesize=A4)
    elements = []

    elements.append(Paragraph("Job Market Analytics Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Top 10 Skills in Demand", styles["Heading2"]))
    elements.append(Image("reports/top_skills.png", width=400, height=250))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Top 10 Job Titles", styles["Heading2"]))
    elements.append(Image("reports/top_titles.png", width=400, height=250))

    doc.build(elements)

    print(f"✅ Report generated at {REPORT_PATH}")

def main():
    generate_report()

if __name__ == "__main__":
    main()
