import requests
import pandas as pd
import os
from src.config import DATA_DIR
from dotenv import load_dotenv

# Load .env for API credentials
load_dotenv()

API_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

from src.config import DATA_DIR
import os

CSV_PATH = os.path.join(DATA_DIR, "jobs.csv")
JSON_PATH = os.path.join(DATA_DIR, "jobs.json")


# Define multiple job roles and countries
JOB_ROLES = [
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "business analyst",
    "software engineer"
]

COUNTRIES = ["in", "us", "gb", "ca", "au"]  # India, USA, UK, Canada, Australia


def fetch_jobs(job_role, country="in", results_per_page=20, page=1):
    """
    Fetch jobs from Adzuna API and return a DataFrame
    """
    if not API_ID or not API_KEY:
        raise Exception("❌ Missing Adzuna API credentials. Please set ADZUNA_APP_ID and ADZUNA_APP_KEY in your .env")

    url = f"{BASE_URL}/{country}/search/{page}"
    params = {
        "app_id": API_ID,
        "app_key": API_KEY,
        "results_per_page": results_per_page,
        "what": job_role,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Error fetching jobs for {job_role} in {country}: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    results = data.get("results", [])

    jobs = []
    for job in results:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "created": job.get("created"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "description": job.get("description"),
            "redirect_url": job.get("redirect_url"),
            "search_role": job_role,   # keep track of which role we searched
            "search_country": country  # keep track of which country we searched
        })

    return pd.DataFrame(jobs)


def main(results_per_page=50):
    all_jobs = []

    for role in JOB_ROLES:
        for country in COUNTRIES:
            print(f"🚀 Fetching jobs for role: '{role}' in {country.upper()} ...")
            df = fetch_jobs(role, country, results_per_page)
            if not df.empty:
                all_jobs.append(df)

    if not all_jobs:
        print("⚠️ No jobs fetched, nothing to save.")
        return

    final_df = pd.concat(all_jobs, ignore_index=True)
    final_df.to_csv(CSV_PATH, index=False)
    final_df.to_json(JSON_PATH, orient="records", indent=2)
    print(f"✅ {len(final_df)} jobs saved to {CSV_PATH} & {JSON_PATH}")


if __name__ == "__main__":
    main()
