# src/config.py
import os

# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database path
DB_PATH = os.path.join(BASE_DIR, "..", "data", "jobs.db")

# SQLAlchemy connection URL
DB_URL = f"sqlite:///{DB_PATH}"

# Data directory (always the same for fetch & process)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Ensure the folder exists
os.makedirs(DATA_DIR, exist_ok=True)
