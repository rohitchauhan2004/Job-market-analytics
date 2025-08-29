# src/aggregate/build_weekly.py
import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DB_URL

def main():
    engine = create_engine(DB_URL, future=True)
    jc = pd.read_sql("select id, posted_at, salary_min, salary_max from jobs_clean", engine)
    js = pd.read_sql("""select job_skills.job_id, skills.id as skill_id
                        from job_skills join skills on skills.id = job_skills.skill_id""", engine)
    if jc.empty or js.empty:
        print("No data to aggregate"); return

    df = js.merge(jc, left_on="job_id", right_on="id", how="inner")
    df["posted_at"] = pd.to_datetime(df["posted_at"], errors="coerce")
    df["week_start"] = df["posted_at"].dt.to_period("W").apply(lambda p: p.start_time.date())
    df["sal"] = df["salary_min"].fillna(df["salary_max"])

    ag = (df.groupby(["week_start","skill_id"])
            .agg(demand=("job_id","count"),
                 median_salary=("sal","median"),
                 p25_salary=("sal",lambda s: s.quantile(0.25)),
                 p75_salary=("sal",lambda s: s.quantile(0.75)))
            .reset_index())

    with engine.begin() as conn:
        for _, r in ag.iterrows():
            conn.execute(text("""
                insert or replace into weekly_skill_demand
                (week_start, skill_id, demand, median_salary, p25_salary, p75_salary)
                values (:w,:s,:d,:m,:p25,:p75)
            """), {"w": str(r.week_start), "s": int(r.skill_id), "d": int(r.demand),
                   "m": (None if pd.isna(r.median_salary) else float(r.median_salary)),
                   "p25": (None if pd.isna(r.p25_salary) else float(r.p25_salary)),
                   "p75": (None if pd.isna(r.p75_salary) else float(r.p75_salary))})
    print("✅ Built weekly_skill_demand")

if __name__ == "__main__":
    main()
