import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sqlite3
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
import plotly.express as px
from prophet import Prophet
import spacy
import subprocess

# -------------------------
# Config
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jobs.db")

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
    st.stop()

# -------------------------
# Helper: Run ETL
# -------------------------
def run_etl():
    """Run the ETL script to fetch latest jobs."""
    try:
        result = subprocess.run(
            ["python", "etl.py"],  # change etl.py to your actual script name
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

# -------------------------
# Load Data from SQLite
# -------------------------
@st.cache_data
def load_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM jobs", conn)
        conn.close()
        return df
    else:
        return pd.DataFrame()

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("⚙️ Controls")

if st.sidebar.button("🔄 Fetch Latest Jobs (Run ETL)"):
    with st.spinner("Fetching latest jobs..."):
        success, msg = run_etl()
        if success:
            st.sidebar.success("✅ ETL pipeline finished!")
            st.cache_data.clear()  # clear cache so we reload fresh data
        else:
            st.sidebar.error("❌ ETL pipeline failed")
            st.sidebar.text(msg)

# -------------------------
# Auto-run ETL if no data
# -------------------------
df = load_data()
if df.empty:
    st.warning("⚠️ No jobs data found. Running ETL now...")
    success, msg = run_etl()
    if success:
        st.success("✅ ETL pipeline finished. Please refresh the page.")
        st.stop()
    else:
        st.error("❌ ETL pipeline failed")
        st.text(msg)
        st.stop()

# -------------------------
# Dashboard starts here
# -------------------------
st.title("📊 Job Market Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("🔎 Filter Jobs")
roles = df["title"].dropna().unique()
selected_roles = st.sidebar.multiselect("Filter by Job Role", roles)

locations = df["location"].dropna().unique()
selected_locations = st.sidebar.multiselect("Filter by Location", locations)

companies = df["company"].dropna().unique()
selected_companies = st.sidebar.multiselect("Filter by Company", companies)

if "salary_min" in df.columns and "salary_max" in df.columns and (
    df["salary_min"].notna().any() or df["salary_max"].notna().any()
):
    salary_min = int(df["salary_min"].fillna(0).min())
    salary_max = int(df["salary_max"].fillna(0).max())
    selected_salary = st.sidebar.slider(
        "Filter by Salary Range", salary_min, salary_max, (salary_min, salary_max)
    )
else:
    selected_salary = None

filtered_df = df.copy()
if selected_roles:
    filtered_df = filtered_df[filtered_df["title"].isin(selected_roles)]
if selected_locations:
    filtered_df = filtered_df[filtered_df["location"].isin(selected_locations)]
if selected_companies:
    filtered_df = filtered_df[filtered_df["company"].isin(selected_companies)]
if selected_salary:
    filtered_df = filtered_df[
        (filtered_df["salary_min"].fillna(0) >= selected_salary[0])
        & (filtered_df["salary_max"].fillna(1_000_000) <= selected_salary[1])
    ]

st.subheader(f"📋 Showing {len(filtered_df)} job postings")
st.dataframe(filtered_df)

# -------------------------
# KPI Cards
# -------------------------
st.markdown("---")
st.subheader("📊 Key Insights")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div style="background:#f8f9fa;padding:25px;border-radius:12px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)">
            <h3 style="color:#333; margin-bottom:5px;">📌 Total Jobs</h3>
            <h1 style="color:#111; margin:0;">{len(filtered_df)}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    avg_salary = filtered_df[["salary_min", "salary_max"]].mean().mean()
    avg_salary_text = f"${int(avg_salary):,}" if pd.notna(avg_salary) else "N/A"
    st.markdown(
        f"""
        <div style="background:#f8f9fa;padding:25px;border-radius:12px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)">
            <h3 style="color:#27ae60; margin-bottom:5px;">💰 Avg. Salary</h3>
            <h1 style="color:#27ae60; margin:0;">{avg_salary_text}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    top_location = (
        filtered_df["location"].mode()[0]
        if not filtered_df["location"].dropna().empty
        else "N/A"
    )
    st.markdown(
        f"""
        <div style="background:#f8f9fa;padding:25px;border-radius:12px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)">
            <h3 style="color:#2980b9; margin-bottom:5px;">📍 Top Location</h3>
            <h2 style="color:#2980b9; margin:0;">{top_location}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    top_company = (
        filtered_df["company"].mode()[0]
        if not filtered_df["company"].dropna().empty
        else "N/A"
    )
    st.markdown(
        f"""
        <div style="background:#f8f9fa;padding:25px;border-radius:12px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1)">
            <h3 style="color:#8e44ad; margin-bottom:5px;">🏢 Top Company</h3>
            <h2 style="color:#8e44ad; margin:0;">{top_company}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# Charts
# -------------------------
st.markdown("---")
st.subheader("📈 Job Insights")

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.markdown("**📍 Jobs by Location (Top 10)**")
    if not filtered_df["location"].dropna().empty:
        location_counts = filtered_df["location"].value_counts().head(10)
        fig = px.bar(location_counts, x=location_counts.index, y=location_counts.values,
                     labels={"x": "Location", "y": "Job Count"}, color=location_counts.values,
                     color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

with row1_col2:
    st.markdown("**🏢 Jobs by Top Companies**")
    if not filtered_df["company"].dropna().empty:
        company_counts = filtered_df["company"].value_counts().head(10)
        fig = px.bar(company_counts, x=company_counts.index, y=company_counts.values,
                     labels={"x": "Company", "y": "Job Count"}, color=company_counts.values,
                     color_continuous_scale="Purples")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Forecast Section
# -------------------------
st.markdown("---")
st.subheader("🔮 Job Postings Forecast")
try:
    forecast_df = df.copy()
    forecast_df["created"] = pd.to_datetime(forecast_df["created"], errors="coerce")
    daily_counts = forecast_df.groupby(forecast_df["created"].dt.date).size().reset_index(name="y")
    daily_counts.rename(columns={"created": "ds"}, inplace=True)

    if not daily_counts.empty:
        model = Prophet()
        model.fit(daily_counts)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        fig1 = px.line(forecast, x="ds", y="yhat", title="Job Postings Forecast (Next 30 Days)")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("⚠️ Not enough data for forecasting.")
except Exception as e:
    st.error(f"⚠️ Could not generate forecast: {e}")

# -------------------------
# NLP Skill Extraction
# -------------------------
st.markdown("---")
st.subheader("🛠️ Top 10 Skills in Demand (NLP Extracted)")

def extract_skills_from_text(text, skill_list):
    doc = nlp(text)
    found_skills = []
    for token in doc:
        if token.text.lower() in [s.lower() for s in skill_list]:
            found_skills.append(token.text)
    return found_skills

skill_list = [
    "Python", "SQL", "Excel", "Machine Learning", "Deep Learning", "AI",
    "TensorFlow", "PyTorch", "NLP", "Data Analysis", "Statistics",
    "Tableau", "Power BI", "AWS", "Azure", "GCP", "Java", "C++",
    "R", "Hadoop", "Spark", "Scala", "Docker", "Kubernetes"
]

all_skills = []
if "description" in df.columns:
    for desc in df["description"].dropna():
        all_skills.extend(extract_skills_from_text(desc, skill_list))

if all_skills:
    skill_counts = pd.Series(all_skills).str.strip().value_counts().head(10)
    fig_skills = px.bar(
        x=skill_counts.values, y=skill_counts.index, orientation="h",
        labels={"x": "Job Count", "y": "Skill"},
        title="Top 10 Skills in Demand",
        color=skill_counts.values, color_continuous_scale="viridis"
    )
    st.plotly_chart(fig_skills, use_container_width=True)
else:
    st.info("ℹ️ No skills data could be extracted.")
