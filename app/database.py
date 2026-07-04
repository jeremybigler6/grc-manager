import os
import shutil
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_data_dir():
    for candidate in [BASE_DIR / "data", BASE_DIR.parent / "data"]:
        if candidate.exists():
            return candidate
    return BASE_DIR / "data"


DATA_DIR = get_data_dir()
DB_NAME = str(DATA_DIR / "grc_manager.db")


def connect_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(DB_NAME):
        legacy_db = BASE_DIR / "grc_manager.db"
        if legacy_db.exists():
            shutil.copy2(legacy_db, DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Risk Register Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risks (
            risk_id TEXT PRIMARY KEY,
            risk_name TEXT,
            category TEXT,
            likelihood INTEGER,
            impact INTEGER,
            risk_score INTEGER,
            risk_level TEXT,
            owner TEXT,
            treatment_plan TEXT,
            status TEXT,
            date_created TEXT,
            last_review_date TEXT,
            target_date TEXT
        )
    """)

    # Control Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controls (
            control_id TEXT PRIMARY KEY,
            control_name TEXT,
            control_type TEXT,
            framework TEXT,
            owner TEXT,
            status TEXT,
            description TEXT
        )
    """)

    # Risk-Control Mapping Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_control_mapping (
            risk_id TEXT,
            control_id TEXT,
            PRIMARY KEY (risk_id, control_id),
            FOREIGN KEY (risk_id) REFERENCES risks(risk_id),
            FOREIGN KEY (control_id) REFERENCES controls(control_id)
        )
    """)

    conn.commit()
    conn.close()