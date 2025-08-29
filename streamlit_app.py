import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter

def run_etl():
    """Run the ETL pipeline by calling run_pipeline.py"""
    import subprocess

    try:
        result = subprocess.run(
            ["python", "run_pipeline.py", "all"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, "✅ ETL pipeline completed successfully!"
        else:
            return False, f"❌ ETL pipeline failed:\n{result.stderr}"
    except Exception as e:
        return False, f"❌ Error running ETL: {e}"


# Define DB path relative to repo root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jobs.db")

# --------------------------------------------------------------------
# Load Data
# --------------------------------------------------------------------
@st.cache_data
def load_data():
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql("SELECT * FROM jobs", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"❌ Error reading database: {e}")
            return pd.DataFrame()
    else:
        # Run ETL if DB missing
        st.warning("⚠️ No jobs data found. Running ETL now...")
        success, msg = run_etl()
        if not success:
            st.error(msg)
            return pd.DataFrame()
        else:
            st.success(msg)
            try:
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql("SELECT * FROM jobs", conn)
                conn.close()
                return df
            except Exception as e:
                st.error(f"❌ Error loading DB after ETL: {e}")
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
            st.cache_data.clear()
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
roles = df["title"].dropna().unique() if "title" in df.columns else []
selected_roles = st.sidebar.multiselect("Filter by Job Role", roles)

locations = df["location"].dropna().unique() if "location" in df.columns else []
selected_locations = st.sidebar.multiselect("Filter by Location", locations)

companies = df["company"].dropna().unique() if "company" in df.columns else []
selected_companies = st.sidebar.multiselect("Filter by Company", companies)

# Salary filter (only if columns exist)
if {"salary_min", "salary_max"}.issubset(df.columns):
    if df[["salary_min", "salary_max"]].notna().any().any():
        salary_min = int(df["salary_min"].fillna(0).min())
        salary_max = int(df["salary_max"].fillna(0).max())
        selected_salary = st.sidebar.slider(
            "Filter by Salary Range", salary_min, salary_max, (salary_min, salary_max)
        )
    else:
        selected_salary = None
else:
    selected_salary = None

# Apply filters
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
    st.metric("📌 Total Jobs", f"{len(filtered_df):,}")

with kpi2:
    avg_salary = filtered_df[["salary_min", "salary_max"]].mean().mean()
    avg_salary_text = f"${int(avg_salary):,}" if pd.notna(avg_salary) else "N/A"
    st.metric("💰 Avg. Salary", avg_salary_text)

with kpi3:
    top_location = (
        filtered_df["location"].mode()[0]
        if "location" in filtered_df and not filtered_df["location"].dropna().empty
        else "N/A"
    )
    st.metric("📍 Top Location", top_location)

with kpi4:
    top_company = (
        filtered_df["company"].mode()[0]
        if "company" in filtered_df and not filtered_df["company"].dropna().empty
        else "N/A"
    )
    st.metric("🏢 Top Company", top_company)

# -------------------------
# Charts
# -------------------------
st.markdown("---")
st.subheader("📈 Job Insights")

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.markdown("**📍 Jobs by Location (Top 10)**")
    if "location" in filtered_df and not filtered_df["location"].dropna().empty:
        location_counts = filtered_df["location"].value_counts().head(10)
        fig = px.bar(location_counts, x=location_counts.index, y=location_counts.values,
                     labels={"x": "Location", "y": "Job Count"}, color=location_counts.values,
                     color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

with row1_col2:
    st.markdown("**🏢 Jobs by Top Companies**")
    if "company" in filtered_df and not filtered_df["company"].dropna().empty:
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
    if "created" in df.columns:
        forecast_df = df.copy()
        forecast_df["created"] = pd.to_datetime(forecast_df["created"], errors="coerce")
        daily_counts = forecast_df.groupby(forecast_df["created"].dt.date).size().reset_index(name="y")
        daily_counts.rename(columns={"created": "ds"}, inplace=True)

        if len(daily_counts) > 5:
            model = Prophet()
            model.fit(daily_counts)
            future = model.make_future_dataframe(periods=30)
            forecast = model.predict(future)

            fig1 = px.line(forecast, x="ds", y="yhat", title="Job Postings Forecast (Next 30 Days)")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("⚠️ Not enough data for forecasting.")
    else:
        st.info("⚠️ No timestamp column ('created') available for forecasting.")
except Exception as e:
    st.error(f"⚠️ Could not generate forecast: {e}")

# -------------------------
# NLP Skill Extraction
# -------------------------
st.markdown("---")
st.subheader("🛠️ Top 10 Skills in Demand (NLP Extracted)")

def extract_skills_from_text(text, skill_list):
    doc = nlp(text)
    return [token.text for token in doc if token.text.lower() in [s.lower() for s in skill_list]]

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
