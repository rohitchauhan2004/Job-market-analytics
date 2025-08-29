import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Ensure output folder exists
os.makedirs("reports/plots", exist_ok=True)

# Connect to DB
conn = sqlite3.connect("data/jobs.db")

# ---- Top 10 skills ----
skills = pd.read_sql("""
    SELECT s.name AS skill, COUNT(*) AS demand
    FROM job_skills js
    JOIN skills s ON js.skill_id = s.id
    GROUP BY s.name
    ORDER BY demand DESC
    LIMIT 10;
""", conn)

plt.figure(figsize=(10,6))
plt.barh(skills["skill"], skills["demand"])
plt.xlabel("Demand")
plt.title("Top 10 Skills")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("reports/plots/top_skills.png")
plt.show()

# ---- Top 10 job titles ----
titles = pd.read_sql("""
    SELECT title_normalized AS title, COUNT(*) AS count
    FROM jobs_clean
    GROUP BY title_normalized
    ORDER BY count DESC
    LIMIT 10;
""", conn)

plt.figure(figsize=(10,6))
plt.barh(titles["title"], titles["count"])
plt.xlabel("Count")
plt.title("Top 10 Job Titles")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("reports/plots/top_titles.png")
plt.show()

conn.close()
