import sqlite3
import pandas as pd

# Connect to your jobs.db
conn = sqlite3.connect("data/jobs.db")

# Top 10 skills
skills = pd.read_sql("""
    SELECT skill, COUNT(*) AS demand
    FROM job_skills
    GROUP BY skill
    ORDER BY demand DESC
    LIMIT 10
""", conn)

print("\n🔥 Top 10 Skills in Demand:")
print(skills)

# Example: top companies
companies = pd.read_sql("""
    SELECT company, COUNT(*) AS postings
    FROM jobs_clean
    GROUP BY company
    ORDER BY postings DESC
    LIMIT 10
""", conn)

print("\n🏢 Top Hiring Companies:")
print(companies)

conn.close()
