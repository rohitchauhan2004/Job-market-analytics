import os
import pandas as pd
import sqlite3
from prophet import Prophet
import matplotlib.pyplot as plt
from src.config import DB_PATH

def main():
    # Load jobs data from SQLite
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT created FROM jobs", conn)
    conn.close()

    # Convert dates (remove timezone if present)
    df["created"] = pd.to_datetime(df["created"]).dt.tz_localize(None)

    # Count postings per day
    daily_counts = df.groupby("created").size().reset_index(name="y")
    daily_counts.rename(columns={"created": "ds"}, inplace=True)

    # Train Prophet model
    model = Prophet()
    model.fit(daily_counts)

    # Forecast next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Plot results
    fig = model.plot(forecast)
    plt.title("Job Postings Forecast")
    plt.savefig(os.path.join("data", "forecast.png"))
    plt.show()

    print("✅ Forecast completed → saved to data/forecast.png")

if __name__ == "__main__":
    main()
