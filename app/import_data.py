import csv
import sqlite3
from pathlib import Path
from database import DB_NAME
from audit_trail import log_activity


def get_data_dir():
    base_dir = Path(__file__).resolve().parent
    for candidate in [base_dir / "data", base_dir.parent / "data"]:
        if candidate.exists():
            return candidate
    return base_dir / "data"


DATA_DIR = get_data_dir()


def import_controls_from_csv():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM risk_control_mapping")
        cursor.execute("DELETE FROM controls")

        with open(DATA_DIR / "controls_library.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO controls
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, row)

        conn.commit()

    print("Controls imported successfully.")
    log_activity("Data Imported", "Controls CSV imported")


def import_mappings_from_csv():
    count = 0

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM risk_control_mapping")

        with open(DATA_DIR / "risk_control_mapping.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) < 2:
                    continue

                risk_id = row[0].strip().upper()
                control_id = row[1].strip().upper()

                cursor.execute("""
                    INSERT OR REPLACE INTO risk_control_mapping
                    VALUES (?, ?)
                """, (risk_id, control_id))

                count += 1

        conn.commit()

    print(f"Risk-control mappings imported successfully. {count} mappings added.")
    log_activity("Data Imported", f"Risk-control mappings imported ({count})")


def import_risks_from_csv():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM risk_control_mapping")
        cursor.execute("DELETE FROM risks")

        with open(DATA_DIR / "risk_register.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO risks
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)

        conn.commit()

    print("Risks imported successfully.")
    log_activity("Data Imported", "Risks CSV imported")


def import_all_data():
    import_controls_from_csv()
    import_risks_from_csv()
    import_mappings_from_csv()
    print("All CSV data imported successfully.")