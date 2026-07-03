import csv
import sqlite3
from database import DB_NAME


def import_controls_from_csv():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        with open("controls_library.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO controls
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, row)

        conn.commit()

    print("Controls imported successfully.")


def import_mappings_from_csv():
    count = 0

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        with open("risk_control_mapping.csv", "r", newline="") as file:
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


def import_risks_from_csv():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        with open("risk_register.csv", "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cursor.execute("""
                    INSERT OR REPLACE INTO risks
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)

        conn.commit()

    print("Risks imported successfully.")


def import_all_data():
    import_controls_from_csv()
    import_risks_from_csv()
    import_mappings_from_csv()
    print("All CSV data imported successfully.")