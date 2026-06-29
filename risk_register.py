import csv
import os

FILE_NAME = "risk_register.csv"

HEADERS = [
    "Risk ID",
    "Risk Name",
    "Category",
    "Likelihood",
    "Impact",
    "Risk Score",
    "Risk Level",
    "Owner",
    "Treatment Plan",
    "Status"
]


def calculate_risk_level(score):
    if score >= 15:
        return "High"
    elif score >= 8:
        return "Medium"
    else:
        return "Low"


def create_file_if_missing():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)


def add_risk():
    print("\n--- Add New Risk ---")

    risk_id = input("Risk ID: ")
    risk_name = input("Risk Name: ")
    category = input("Category: ")

    likelihood = int(input("Likelihood (1-5): "))
    impact = int(input("Impact (1-5): "))

    risk_score = likelihood * impact
    risk_level = calculate_risk_level(risk_score)

    owner = input("Risk Owner: ")
    treatment_plan = input("Treatment Plan: ")
    status = input("Status: ")

    risk = [
        risk_id,
        risk_name,
        category,
        likelihood,
        impact,
        risk_score,
        risk_level,
        owner,
        treatment_plan,
        status
    ]

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(risk)

    print(f"\nRisk added successfully. Risk Level: {risk_level}")


def view_risks():
    print("\n--- Risk Register ---")

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            print(row)

def edit_risk():
    print("\n----------- View / Edit Risk -----------")
    print("Press Enter to keep the current value.")
    print("Type 'q' at any prompt to cancel editing.")
    print("----------------------------------------\n")

    risk_id = input("Enter the Risk ID to view/edit: ").strip().upper()

    risks = []
    found = False

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0].strip().upper() == risk_id:
                found = True

                print("\nCurrent Risk Information")
                print("------------------------")
                print(f"Risk ID:        {row[0]}")
                print(f"Risk Name:      {row[1]}")
                print(f"Category:       {row[2]}")
                print(f"Likelihood:     {row[3]}")
                print(f"Impact:         {row[4]}")
                print(f"Risk Score:     {row[5]}")
                print(f"Risk Level:     {row[6]}")
                print(f"Owner:          {row[7]}")
                print(f"Treatment Plan: {row[8]}")
                print(f"Status:         {row[9]}")

                choice = input("\nEdit this risk? (Y/N): ").lower()

                if choice != "y":
                    print("No changes made.")
                    return

                new_value = input(f"Risk Name ({row[1]}): ")
                if new_value.lower() == "q":
                    print("Edit cancelled.")
                    return
                row[1] = new_value or row[1]

                new_value = input(f"Category ({row[2]}): ")
                if new_value.lower() == "q":
                    print("Edit cancelled.")
                    return
                row[2] = new_value or row[2]

                likelihood = input(f"Likelihood ({row[3]}): ")
                if likelihood.lower() == "q":
                    print("Edit cancelled.")
                    return

                impact = input(f"Impact ({row[4]}): ")
                if impact.lower() == "q":
                    print("Edit cancelled.")
                    return

                if likelihood:
                    row[3] = int(likelihood)

                if impact:
                    row[4] = int(impact)

                row[5] = int(row[3]) * int(row[4])
                row[6] = calculate_risk_level(row[5])

                new_value = input(f"Risk Owner ({row[7]}): ")
                if new_value.lower() == "q":
                    print("Edit cancelled.")
                    return
                row[7] = new_value or row[7]

                new_value = input(f"Treatment Plan ({row[8]}): ")
                if new_value.lower() == "q":
                    print("Edit cancelled.")
                    return
                row[8] = new_value or row[8]

                new_value = input(f"Status ({row[9]}): ")
                if new_value.lower() == "q":
                    print("Edit cancelled.")
                    return
                row[9] = new_value or row[9]

            risks.append(row)

    if not found:
        print("Risk ID not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(risks)

    print("Risk updated successfully.")


def main():
    create_file_if_missing()

    while True:
        print("\n=== Python GRC Risk Register ===")
        print("1. Add Risk")
        print("2. View Risks")
        print("3. Edit Risk")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_risk()
        elif choice == "2":
            view_risks()
        elif choice == "3":
            edit_risk()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


main()