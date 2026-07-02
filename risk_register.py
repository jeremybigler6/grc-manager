import csv
import os
from datetime import date
from controls import get_controls_for_risk


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
    "Status",
    "Date Created",
    "Last Updated",
    "Completion Date"
]


def calculate_risk_level(score):
    if score >= 20:
        return "Critical"
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
    print("Type 'q' at any prompt to cancel adding a new risk.\n")

    risk_id = input("Risk ID: ")
    if risk_id.lower() == "q":
        print("Add risk cancelled.")
        return

    risk_name = input("Risk Name: ")
    if risk_name.lower() == "q":
        print("Add risk cancelled.")
        return

    category = input("Category: ")
    if category.lower() == "q":
        print("Add risk cancelled.")
        return

    likelihood = int(input("Likelihood (1-5): "))
    if likelihood < 1 or likelihood > 5:
        print("Invalid likelihood. Please enter a value between 1 and 5.")
        return

    impact = int(input("Impact (1-5): "))
    if impact < 1 or impact > 5:
        print("Invalid impact. Please enter a value between 1 and 5.")
        return

    risk_score = likelihood * impact
    risk_level = calculate_risk_level(risk_score)

    owner = input("Risk Owner: ")
    treatment_plan = input("Treatment Plan: ")
    status = input("Status: ")

    target_completion_date = input("Target Completion Date (YYYY-MM-DD): ")

    today = date.today().isoformat()

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
        status,
        today,
        today,
        target_completion_date
    ]

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(risk)

    print(f"\nRisk added successfully. Risk Level: {risk_level}")


def view_risks():
    risks = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            risks.append(row)

    if not risks:
        print("\nNo risks found.")
        return

    print("\n========== View Risks ==========")
    print("1. Sort by Risk ID")
    print("2. Sort by Risk Score")
    print("3. Sort by Risk Level")
    print("4. Sort by Due Date")
    print("5. Sort by Owner")
    print("6. No Sorting")
    print("================================")

    choice = input("Choose a sorting option: ").strip()

    if choice == "1":
        risks = sorted(risks, key=lambda row: row[0])
    elif choice == "2":
        risks = sorted(risks, key=lambda row: int(row[5]), reverse=True)
    elif choice == "3":
        level_order = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }
        risks = sorted(
            risks,
            key=lambda row: level_order.get(row[6].strip().lower(), 0),
            reverse=True
        )
    elif choice == "4":
        risks = sorted(risks, key=lambda row: date.fromisoformat(row[12]))
    elif choice == "5":
        risks = sorted(risks, key=lambda row: row[7].strip().lower())
    elif choice == "6":
        pass
    else:
        print("Invalid sorting option. Showing unsorted risks.")

    display_risks("Risk Register", risks)
    

def edit_risk(risk_id=None):
    risk_id_was_passed_in = risk_id is not None

    if risk_id is None:
        print("\n----------- View / Edit Risk -----------")
        print("Type 'q' at any prompt to cancel editing.")
        print("----------------------------------------\n")
        risk_id = input("Enter the Risk ID to view/edit: ").strip().upper()
    else:
        risk_id = risk_id.strip().upper()

    if risk_id.lower() == "q":
        print("Edit cancelled.")
        return

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
                print(f"Completion Date: {row[12]}")

                if not risk_id_was_passed_in:
                    choice = input("\nEdit this risk? (Y/N): ").lower().strip()

                    if choice != "y":
                        print("No changes made.")
                        return

                print("\nWhat would you like to edit?")
                print("1. Risk Name")
                print("2. Category")
                print("3. Likelihood")
                print("4. Impact")
                print("5. Risk Owner")
                print("6. Treatment Plan")
                print("7. Status")
                print("8. Cancel")

                edit_choice = input("Choose an option: ").strip()

                if edit_choice == "1":
                    new_value = input(f"New Risk Name ({row[1]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    row[1] = new_value or row[1]

                elif edit_choice == "2":
                    new_value = input(f"New Category ({row[2]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    row[2] = new_value or row[2]

                elif edit_choice == "3":
                    new_value = input(f"New Likelihood ({row[3]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    if new_value:
                        row[3] = int(new_value)
                        row[5] = int(row[3]) * int(row[4])
                        row[6] = calculate_risk_level(row[5])

                elif edit_choice == "4":
                    new_value = input(f"New Impact ({row[4]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    if new_value:
                        row[4] = int(new_value)
                        row[5] = int(row[3]) * int(row[4])
                        row[6] = calculate_risk_level(row[5])

                elif edit_choice == "5":
                    new_value = input(f"New Risk Owner ({row[7]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    row[7] = new_value or row[7]

                elif edit_choice == "6":
                    new_value = input(f"New Treatment Plan ({row[8]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    row[8] = new_value or row[8]

                elif edit_choice == "7":
                    new_value = input(f"New Status ({row[9]}): ")
                    if new_value.lower() == "q":
                        print("Edit cancelled.")
                        return
                    row[9] = new_value or row[9]

                elif edit_choice == "8":
                    print("Edit cancelled.")
                    return

                else:
                    print("Invalid edit option.")
                    return

            risks.append(row)

    if not found:
        print("Risk ID not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(risks)

    print("Risk updated successfully.")

def delete_risk():
    print("\n----------- Delete Risk -----------")
    print("Type 'q' to cancel.")
    print("-----------------------------------\n")

    risk_id = input("Enter the Risk ID to delete: ").strip().upper()

    if risk_id.lower() == "q":
        print("Delete cancelled.")
        return

    risks = []
    found = False
    deleted_risk = None

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0].strip().upper() == risk_id:
                found = True
                deleted_risk = row

                print("\nRisk Found")
                print("----------")
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

                confirm = input("\nAre you sure you want to delete this risk? (Y/N): ").strip().lower()

                if confirm == "y":
                    print("Risk deleted.")
                    continue
                else:
                    print("Delete cancelled.")
                    risks.append(row)
            else:
                risks.append(row)

    if not found:
        print("Risk ID not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(risks)


def view_risk_details():

    risk_id = input("Enter Risk ID: ").strip().upper()

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:

            if row[0].strip().upper() == risk_id:

                print("\n========== Risk Details ==========\n")

                print(f"Risk ID:         {row[0]}")
                print(f"Risk Name:       {row[1]}")
                print(f"Category:        {row[2]}")

                print()

                print(f"Likelihood:      {row[3]}")
                print(f"Impact:          {row[4]}")
                print(f"Risk Score:      {row[5]}")
                print(f"Risk Level:      {row[6]}")

                print()

                print(f"Owner:           {row[7]}")
                print(f"Status:          {row[9]}")

                print()

                print(f"Date Created:    {row[10]}")
                print(f"Last Updated:    {row[11]}")
                print(f"Completion Date: {row[12]}")

                print()

                print("Treatment Plan")
                print("-" * 40)
                print(row[8])

                controls = get_controls_for_risk(risk_id)

                print("Associated Controls")
                print("-" * 40)

                if not controls:
                    print("None")

                else:
                    for control in controls:
                        print(f"✓ {control[0]} - {control[1]}")

                return

    print("Risk not found.")


def search_risks():
    print("\n----------- Search Risks -----------")
    print("1. Search by Risk ID")
    print("2. Search by Risk Name")
    print("3. Search by Category")
    print("4. Search by Owner")
    print("5. Search by Status")
    print("------------------------------------")

    choice = input("Choose a search option: ")

    if choice == "1":
        column = 0
        search_label = "Risk ID"
    elif choice == "2":
        column = 1
        search_label = "Risk Name"
    elif choice == "3":
        column = 2
        search_label = "Category"
    elif choice == "4":
        column = 7
        search_label = "Owner"
    elif choice == "5":
        column = 9
        search_label = "Status"
    else:
        print("Invalid search option.")
        return

    search_term = input(f"Enter {search_label} to search for: ").strip().lower()

    found = False

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if search_term in row[column].lower():
                found = True
                print("\nRisk Found")
                print("----------")
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
    
                action = input("\nWould you like to edit this risk? (Y/N): ").strip().lower()

                if action == "y":
                    edit_risk(row[0])
                    return

    if not found:
        print("No matching risks found.")

def summary_dashboard():

    overdue_risks = []
    upcoming_risks = []
    today = date.today()

    total_risks = 0
    open_risks = 0
    closed_risks = 0
    mitigated_risks = 0

    low_risks = 0
    medium_risks = 0
    high_risks = 0
    critical_risks = 0

    total_score = 0
    highest_score = 0


    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            total_risks += 1

            score = int(row[5])
            total_score += score

            if score > highest_score:
                highest_score = score

            status = row[9].strip().lower()

            if status == "open":
                open_risks += 1
            elif status == "closed":
                closed_risks += 1
            elif status == "mitigated":
                mitigated_risks += 1

            target_date = date.fromisoformat(row[12])
            status = row[9].strip().lower()

            if status != "closed":
                if target_date < today:
                    overdue_risks.append(row)
                elif target_date >= today:
                    days_until_due = (target_date - today).days

                    if days_until_due <= 7:
                        upcoming_risks.append(row)


            level = row[6].strip().lower()

            if level == "low":
                low_risks += 1
            elif level == "medium":
                medium_risks += 1
            elif level == "high":
                high_risks += 1
            elif level == "critical":
                critical_risks += 1

    if total_risks > 0:
        average_score = total_score / total_risks
    else:
        average_score = 0

    print("\n========== Risk Dashboard ==========")
    print(f"Total Risks:          {total_risks}")
    print()
    print(f"Open Risks:           {open_risks}")
    print(f"Closed Risks:         {closed_risks}")
    print(f"Mitigated Risks:      {mitigated_risks}")
    print()
    print(f"Critical Risks:       {critical_risks}")
    print(f"High Risks:           {high_risks}")
    print(f"Medium Risks:         {medium_risks}")
    print(f"Low Risks:            {low_risks}")
    print()
    print(f"Average Risk Score:   {average_score:.1f}")
    print(f"Highest Risk Score:   {highest_score}")
    print(f"Overdue Risks:        {len(overdue_risks)}")
    print(f"Due Soon Risks:       {len(upcoming_risks)}")
    print("====================================")

    if overdue_risks:
        print("\n========== Overdue Risks ==========")

    for row in overdue_risks:
        print(
            f"{row[0]} - {row[1]} | "
            f"Score: {row[5]} | "
            f"Level: {row[6]} | "
            f"Owner: {row[7]} | "
            f"Due: {row[12]}"
        )
        print()

    if upcoming_risks:
        print("\n========== Due Soon Risks ==========")

        for row in upcoming_risks:
            print(
                f"{row[0]} - {row[1]} | "
                f"Score: {row[5]} | "
                f"Level: {row[6]} | "
                f"Owner: {row[7]} | "
                f"Due: {row[12]}"
            )
            print()


def risk_dashboard():
    while True:
        print("\n========== Dashboard Menu ==========")
        print("1. Summary Dashboard")
        print("2. View Overdue Risks")
        print("3. View Due Soon Risks")
        print("4. View Critical Risks")
        print("5. View Risk Heat Map")
        print("6. Return to Main Menu")
        print("====================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            summary_dashboard()
        elif choice == "2":
            view_overdue_risks()
        elif choice == "3":
            view_upcoming_risks()
        elif choice == "4":
            view_critical_risks()
        elif choice == "5":
            risk_heat_map()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")


def risk_heat_map():
    heat_map = {
        (1, 1): 0, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0,
        (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0,
        (3, 1): 0, (3, 2): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0,
        (4, 1): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0,
        (5, 1): 0, (5, 2): 0, (5, 3): 0, (5, 4): 0, (5, 5): 0,
    }

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            likelihood = int(row[3])
            impact = int(row[4])

            heat_map[(impact, likelihood)] += 1

    print("\n========== Risk Heat Map ==========")
    print("Impact")
    print()
    print("        Likelihood")
    print("        1   2   3   4   5")
    print("      ---------------------")

    for impact in range(5, 0, -1):
        print(f"{impact}  |", end="  ")

        for likelihood in range(1, 6):
            count = heat_map[(impact, likelihood)]

            if count == 0:
                print(".", end="   ")
            else:
                print(count, end="   ")

        print()

    print()
    print("Each number shows how many risks are in that impact/likelihood box.")
    print("===================================")
    

def display_risks(title, risks):
    print(f"\n========== {title} ==========")

    if not risks:
        print("No matching risks found.")
        return

    for row in risks:
        print(
            f"{row[0]} - {row[1]} | "
            f"Score: {row[5]} | "
            f"Level: {row[6]} | "
            f"Owner: {row[7]} | "
            f"Due: {row[12]}"
        )

        controls = get_controls_for_risk(row[0])

        print("Associated Controls")

        if not controls:
            print("   None")

        else:
            for control in controls:
                print(f"   ✓ {control[0]} - {control[1]}")

        print()


def view_upcoming_risks():
    upcoming_risks = []
    today = date.today()

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            status = row[9].strip().lower()
            target_date = date.fromisoformat(row[12])

            if status != "closed":
                days_until_due = (target_date - today).days

                if 0 <= days_until_due <= 7:
                    upcoming_risks.append(row)

    display_risks("Due Soon Risks", upcoming_risks)



def view_overdue_risks():
    overdue_risks = []
    today = date.today()

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            status = row[9].strip().lower()
            target_date = date.fromisoformat(row[12])

            if status != "closed" and target_date < today:
                overdue_risks.append(row)

    display_risks("Overdue Risks", overdue_risks)


def view_critical_risks():
    critical_risks = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if row[6].strip().lower() == "critical":
                critical_risks.append(row)

    display_risks("Critical Risks", critical_risks)


    
def risk_register_menu():
    while True:
        print("\n=================================")
        print("      RISK MANAGEMENT")
        print("=================================")

        print("\nView")
        print("----")
        print("1. All Risks")
        print("2. Risk Profile")
        print("3. Search Risks")

        print("\nManage")
        print("------")
        print("4. Add Risk")
        print("5. Edit Risk")
        print("6. Delete Risk")

        print("\nAnalysis")
        print("--------")
        print("7. Risk Dashboard")

        print("\n0. Return")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_risks()

        elif choice == "2":
            view_risk_details()

        elif choice == "3":
            search_risks()

        elif choice == "4":
            add_risk()

        elif choice == "5":
            edit_risk()

        elif choice == "6":
            delete_risk()

        elif choice == "7":
            risk_dashboard()

        elif choice == "0":
            break