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


def main():
    create_file_if_missing()

    while True:
        print("\n=== Python GRC Risk Register ===")
        print("1. Add Risk")
        print("2. View Risks")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_risk()
        elif choice == "2":
            view_risks()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


main()