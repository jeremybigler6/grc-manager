from risk_register import (
    risk_register_menu,
    create_file_if_missing,
    add_risk,
    view_risks,
    edit_risk,
    delete_risk,
    search_risks,
    risk_dashboard
)


from controls import (
    create_control_file_if_missing,
    controls_menu,
    create_mapping_file_if_missing
)


def main():
    create_file_if_missing()
    create_control_file_if_missing()
    create_mapping_file_if_missing()

    while True:
        print("\n=================================")
        print("         GRC MANAGER")
        print("=================================")
        print("1. Risk Management")
        print("2. Control Management")
        print("3. Reports (Coming Soon)")
        print("4. Audit Log (Coming Soon)")
        print("5. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            risk_register_menu()

        elif choice == "2":
            controls_menu()

        elif choice == "3":
            print("\nReports module coming soon.")

        elif choice == "4":
            print("\nAudit Log module coming soon.")

        elif choice == "5":
            print("\nThank you for using GRC Manager.")
            break

        else:
            print("\nInvalid choice.")


main()