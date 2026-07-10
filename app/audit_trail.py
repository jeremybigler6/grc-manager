import sqlite3
from datetime import datetime
from database import DB_NAME, connect_db


def create_audit_table(conn=None):
    if conn is None:
        conn = connect_db()
        owns_connection = True
    else:
        owns_connection = False

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            details TEXT,
            created_at TEXT NOT NULL
        )
    """)

    if owns_connection:
        conn.commit()
        conn.close()


def log_activity(action, details=""):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO audit_log (action, details, created_at)
        VALUES (?, ?, ?)
    """, (action, details, timestamp))

    conn.commit()
    conn.close()


def get_audit_log(limit=20):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT action, details, created_at
        FROM audit_log
        ORDER BY created_at DESC, id DESC
        LIMIT ?
    """, (limit,))

    entries = cursor.fetchall()
    conn.close()
    return entries


def clear_audit_log():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audit_log")
    conn.commit()
    conn.close()
    print("\nAudit log cleared.")


def view_audit_trail(limit=50):
    while True:
        entries = get_audit_log(limit)

        print(f"\n========== Audit Trail (Showing Last {limit} Events) ==========")

        if not entries:
            print("No audit activity recorded yet.")
        else:
            for action, details, created_at in entries:
                print(f"{created_at} | {action} | {details}")

        print("\n---------------------------------")
        print("1. Clear Audit Log Table")
        print("B. Return to Menu")
        print("---------------------------------")
        
        choice = input("Select an option: ").strip().upper()  # Forces uppercase to handle 'b' or 'B'

        if choice == "1":
            confirm = input("\nAre you sure you want to delete the log? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                clear_audit_log_database_table() 
                print("[Database] Audit log cleared successfully.")
            else:
                print("Operation cancelled. Log was not deleted.")
                
        elif choice == "B":
            print("Returning...")
            break
        else:
            print("Invalid choice. Please select 1 or B.")


def reports_and_audit_menu():
    while True:
        print("\n========== Reports & Audit Trail ==========")
        print("1. Risk-Control Coverage Report")
        print("2. Audit Trail Overview")
        print("3. Clear Audit Log")
        print("4. Return to Main Menu")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            from controls import view_all_risks_with_controls
            view_all_risks_with_controls()
        elif choice == "2":
            log_activity("Audit Trail Viewed", "User opened the audit trail overview")
            view_audit_trail()
        elif choice == "3":
            clear_audit_log()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice.")
