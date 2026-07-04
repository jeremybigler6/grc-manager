from database import create_tables
from audit_trail import create_audit_table, clear_audit_log, log_activity, view_audit_trail
from risk_register import risk_register_menu
from controls import controls_menu, view_all_risks_with_controls
from import_data import import_all_data
from ai_tools import ai_tools_menu

def framework_lookup_menu():
    print("\n========== AI Framework Lookup ==========")

    framework = input("Framework name: ")
    control_id = input("Control ID: ")

    result = explain_framework_control(framework, control_id)

    print("\n========== Framework Control Explanation ==========")
    print(result)

def reports_and_audit_menu():
    while True:
        print("\n========== Reports & Audit Trail ==========")
        print("1. Risk-Control Coverage Report")
        print("2. Audit Trail Overview")
        print("3. Clear Audit Log")
        print("4. Return to Main Menu")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
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


def main():
    create_tables()
    create_audit_table()
    log_activity("Application Started", "GRC Manager launched")

    while True:
        print("\n=================================")
        print("         GRC MANAGER")
        print("=================================")
        print("1. Risk Management")
        print("2. Control Management")
        print("3. Risk Treatment Generator")
        print("4. Reports & Audit Trail")
        print("5. Import Data from CSV")
        print("6. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            risk_register_menu()

        elif choice == "2":
            controls_menu()

        elif choice == "3":
            ai_tools_menu()

        elif choice == "4":
            reports_and_audit_menu()

        elif choice == "5":
            import_all_data()

        elif choice == "6":
            print("\nThank you for using GRC Manager.")
            break

        else:
            print("\nInvalid choice.")


main()