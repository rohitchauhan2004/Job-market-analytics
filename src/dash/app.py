
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from src.config import DB_URL

st.set_page_config(page_title="Job Market Analytics", layout="wide")
st.title("📊 Real-Time Job Market Analytics")

engine = create_engine(DB_URL, future=True)

skills = pd.read_sql("select id, name from skills order by name", engine)
if skills.empty:
    st.info("No data yet. Run ingest → process → aggregate → forecast.")
    st.stop()

# Sidebar
skill_name = st.sidebar.selectbox("Choose a skill", skills["name"])
sid = int(skills[skills["name"]==skill_name]["id"].iloc[0])

col1, col2 = st.columns(2)

with col1:
    latest = pd.read_sql("""
        select s.name, w.week_start, w.demand, w.median_salary
        from weekly_skill_demand w
        join skills s on s.id = w.skill_id
        where w.week_start = (select max(week_start) from weekly_skill_demand)
        order by demand desc
        limit 20
    """, engine)
    st.subheader("Top skills this week")
    st.dataframe(latest)

with col2:
    hist = pd.read_sql(f"""
        select week_start, demand, median_salary
        from weekly_skill_demand where skill_id = {sid} order by week_start
    """, engine)
    if not hist.empty:
        hist["week_start"] = pd.to_datetime(hist["week_start"])
        st.subheader(f"Demand over time — {skill_name}")
        st.line_chart(hist.set_index("week_start")["demand"])
        st.subheader("Median salary over time")
        st.line_chart(hist.set_index("week_start")["median_salary"])

st.subheader("Forecast (next 26 weeks)")
fc = pd.read_sql(f"""
    select week_start as ds, yhat, yhat_lower, yhat_upper
    from skill_forecasts where skill_id = {sid} order by ds
""", engine)
if not fc.empty:
    fc["ds"] = pd.to_datetime(fc["ds"])
    st.area_chart(fc.set_index("ds")["yhat"])
else:
    st.info("No forecast yet. Run: python src\\forecast\\train.py")
