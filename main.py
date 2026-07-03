from database import create_tables
from risk_register import risk_register_menu
from controls import controls_menu
from import_data import import_all_data


def main():
    create_tables()

    while True:
        print("\n=================================")
        print("         GRC MANAGER")
        print("=================================")
        print("1. Risk Management")
        print("2. Control Management")
        print("3. Import Data from CSV")
        print("4. Reports (Coming Soon)")
        print("5. Audit Log (Coming Soon)")
        print("6. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            risk_register_menu()

        elif choice == "2":
            controls_menu()

        elif choice == "3":
            import_all_data()

        elif choice == "4":
            print("\nReports module coming soon.")

        elif choice == "5":
            print("\nAudit Log module coming soon.")

        elif choice == "6":
            print("\nThank you for using GRC Manager.")
            break

        else:
            print("\nInvalid choice.")


main()