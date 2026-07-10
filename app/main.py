from database import create_tables
from audit_trail import create_audit_table, clear_audit_log, log_activity, view_audit_trail
from risk_register import risk_register_menu
from controls import controls_menu, view_all_risks_with_controls
from import_data import import_all_data
from ai_tools import ai_tools_menu
from framework_ai_lookup import explain_framework_control
from grc_agent import run_grc_agent, ai_services_menu

# Dead code from previous versions of the application, retained for reference but not currently in use.
# def framework_lookup_menu():
#     print("\n========== AI Framework Lookup ==========")

#     framework = input("Framework name: ")
#     control_id = input("Control ID: ")

#     result = explain_framework_control(framework, control_id)

#     print("\n========== Framework Control Explanation ==========")
#     print(result)

def reports_and_audit_menu():
    print("\n========== Reports & Audit Trail ==========")
    print("1. View Audit Trail")
    print("2. Clear Audit Log")
    print("3. View All Risks with Controls")
    
    choice = input("\nSelect an option: ").strip()
    if choice == "1":
        view_audit_trail()
    elif choice == "2":
        clear_audit_log()
    elif choice == "3":
        view_all_risks_with_controls()
    else:
        print("Invalid choice.")

    
def manual_controls_and_risk_menu():
    while True:
        print("\n=============================================")
        print("   🛠️  MANUAL CONTROLS & RISK MANAGEMENT")
        print("=============================================")
        print("1. Risk Management")
        print("2. Control Management")
        print("B. Back to Main Menu")

        choice = input("\nSelect an option: ").strip().upper()

        if choice == "1":
            risk_register_menu()

        elif choice == "2":
            controls_menu()

        elif choice == "B":
            print("Returning to Main Menu.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or B.")


def ai_services_hub_menu():
    """Unified UI sub-menu linking your automated agent services and manual AI tools."""
    while True:
        print("\n==================================================")
        print("             AI OPERATIONS CENTER                ")
        print("==================================================")
        print("1. Automated & Agentic Engines (GRC Agents)")
        print("2. Open AI Ad-Hoc Workspace")
        print("B. Back to Main Menu")
        print("==================================================")

        choice = input("Select an API service: ").strip().upper()

        if choice == "1":
            # Calls your original option 1 function
            ai_services_menu()

        elif choice == "2":
            # Calls your original option 2 function
            ai_tools_menu()

        elif choice == "B":
            print("Returning to GRC Manager Main Menu.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or B.")


def main():
    log_activity("Application Started", "GRC Manager launched")

    while True:
        print("\n=================================")
        print("         GRC MANAGER")
        print("=================================")
        print("1. AI Operations Center (Automated & Agentic Services)")  
        print("2. Manual Controls & Risk Management")
        print("3. Reports & Audit Trail")
        print("4. Import Data from CSV")
        print("Type 'EXIT' to quit program.")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            ai_services_hub_menu()

        elif choice == "2":
            manual_controls_and_risk_menu()

        elif choice == "3":
            reports_and_audit_menu()

        elif choice == "4":
            import_all_data()

        elif choice.lower() == "exit":
            log_activity("Application Stopped", "GRC Manager closed cleanly")
            print("\nThank you for using GRC Manager.")
            break

        else:
            print("\nInvalid choice. Please choose a valid menu number or type 'EXIT'.")
            

if __name__ == "__main__":
    # 1. Prepare your local database structures right at boot
    create_tables()
    create_audit_table()
    
    # 2. Fire the log once upon startup
    log_activity("Application Started", "GRC Manager launched")

    # 3. Hand control over to the interactive loop
    main()