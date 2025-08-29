import os

# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database path
DB_PATH = os.path.join(BASE_DIR, "..", "jobs.db")

# Data directory (always the same for fetch & process)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Ensure the folder exists
os.makedirs(DATA_DIR, exist_ok=True)
