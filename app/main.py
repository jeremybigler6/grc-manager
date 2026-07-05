from database import create_tables
from audit_trail import create_audit_table, clear_audit_log, log_activity, view_audit_trail
from risk_register import risk_register_menu
from controls import controls_menu, view_all_risks_with_controls
from import_data import import_all_data
from ai_tools import ai_tools_menu
from framework_ai_lookup import explain_framework_control
from grc_agent import run_grc_agent


def framework_lookup_menu():
    print("\n========== AI Framework Lookup ==========")

    framework = input("Framework name: ")
    control_id = input("Control ID: ")

    result = explain_framework_control(framework, control_id)

    print("\n========== Framework Control Explanation ==========")
    print(result)


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
        print("4. Autonomous GRC Agent (Agentic AI)")
        print("5. Reports & Audit Trail")
        print("6. Import Data from CSV")
        print("7. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            risk_register_menu()

        elif choice == "2":
            controls_menu()

        elif choice == "3":
            ai_tools_menu()

        elif choice == "4":
                    print("\n========== Autonomous GRC Agent ==========")
                    print("Give the agent a complex objective (e.g., 'Audit Risk R-001 and remediate gaps')")
                    objective = input("\nEnter Agent Objective: ").strip()
                    
                    if objective:
                        from grc_agent import run_grc_agent  
                        
                        # Capture the agent's final report and print it to the console
                        final_report = run_grc_agent(objective)
                        print("\n=== FINAL AI COMPLIANCE REPORT ===")
                        print(final_report)
                        print("===================================\n")
                    else:
                        print("Objective cannot be blank.")

        elif choice == "5":
            reports_and_audit_menu()

        elif choice == "6":
            import_all_data()

        elif choice == "7":
            print("\nThank you for using GRC Manager.")
            break

        else:
            print("\nInvalid choice.")


main()