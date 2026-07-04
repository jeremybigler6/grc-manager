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


def view_audit_trail(limit=20):
    entries = get_audit_log(limit)

    print("\n========== Audit Trail ==========")

    if not entries:
        print("No audit activity recorded yet.")
        return

    for action, details, created_at in entries:
        print(f"{created_at} | {action} | {details}")
