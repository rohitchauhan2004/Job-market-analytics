# 📊 Job Market Analytics Dashboard

An end-to-end **ETL + Analytics + Dashboard** project that extracts job postings, transforms and stores them in a database, applies **NLP to extract skills**, and visualizes insights in an interactive **Streamlit dashboard**.

---

## 🚀 Features
- 🔄 **ETL Pipeline**: Extract → Transform → Load jobs data into SQLite DB.  
- 🧹 **Data Cleaning**: Preprocessing of job descriptions.  
- 🛠 **Skill Extraction (NLP)**: Identify top skills (e.g., Python, SQL, Excel) from job descriptions.  
- 📈 **Interactive Dashboard**: Explore job trends, skills in demand, and more using **Streamlit + Plotly**.  
- 💾 **Database Storage**: All jobs stored in `data/jobs.db` (SQLite).  
- 📊 **Reports**: Export filtered jobs into Excel for offline use.  

---

## 🖼️ Dashboard Preview  

### 🔹 ETL Status & Controls  
![ETL and Controls](images/etl_controls.png)

### 🔹 Job Trends Over Time  
![Job Trends](images/job_trends.png)

### 🔹 Top 10 Skills in Demand (NLP Extracted)  
![Skills in Demand](images/skills_in_demand.png)

---

## 🗂️ Project Structure

job-market-analytics-starter/
│── data/ # SQLite DB (jobs.db) & raw data
│── exports/ # Exported reports
│── reports/ # ETL/analytics reports
│── sample_data/ # Sample JSON data
│── src/ # ETL & NLP logic
│── taxonomy/ # Skills taxonomy for NLP
│── streamlit_app.py # Dashboard app
│── run_pipeline.py # Orchestrates ETL pipeline
│── run_etl.py # Run ETL manually
│── run.py # Utility runner
│── requirements.txt # Python dependencies
│── jobs.db # SQLite database
│── filtered_jobs.xlsx # Example exported report
│── images/ # Screenshots for README


---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/job-market-analytics-starter.git
   cd job-market-analytics-starter
2.Create virtual environment
Copy code
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
Install dependencies


3.Copy code
pip install -r requirements.txt
Run ETL pipeline

4.Copy code
python run_pipeline.py
This will create/update the SQLite database: data/jobs.db.

5.Start Dashboard
Copy code
streamlit run streamlit_app.py

📊 Dashboard Features

✅ Job Trends over Time

✅ Top Skills in Demand (NLP Extracted)

✅ Export Filtered Jobs to Excel

✅ Interactive Visuals with Plotly

## 🛠 Tech Stack
- **Python 3.10+**
- **Streamlit** – Dashboard UI
- **Plotly** – Data Visualization
- **SQLite** – Database
- **pandas / numpy** – Data Processing
- **spaCy / NLP** – Skills Extraction
- **FastAPI** – REST API to serve job & skills data


🙌 Future Enhancements

🔹 Job posting API integration (live data)

🔹 Advanced NLP for more accurate skill extraction

🔹 ML-based forecasting of job demand

🔹 Deployment on Streamlit Cloud / AWS / Azure

🤝 Contribution

Want to add new features?

Fork the repo

Create a feature branch

Submit a PR 🚀
