import csv
import os


CONTROL_FILE_NAME = "controls_library.csv"


MAPPING_FILE_NAME = "risk_control_mapping.csv"

MAPPING_HEADERS = [
    "Risk ID",
    "Control ID"
]


CONTROL_HEADERS = [
    "Control ID",
    "Control Name",
    "Control Type",
    "Framework",
    "Owner",
    "Status",
    "Description"
]


def create_control_file_if_missing():
    if not os.path.exists(CONTROL_FILE_NAME):
        with open(CONTROL_FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CONTROL_HEADERS)


def create_mapping_file_if_missing():
    if not os.path.exists(MAPPING_FILE_NAME):
        with open(MAPPING_FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(MAPPING_HEADERS)


def add_control():

    print("\n========== Add Control ==========")
    print("Type 'q' at any prompt to cancel.\n")

    control_id = input("Control ID: ").strip().upper()
    if control_id.lower() == "q":
        print("Add control cancelled.")
        return

    control_name = input("Control Name: ").strip()
    if control_name.lower() == "q":
        print("Add control cancelled.")
        return

    control_type = input("Control Type: ").strip()
    framework = input("Framework: ").strip()
    owner = input("Owner: ").strip()
    status = input("Status: ").strip()
    description = input("Description: ").strip()

    control = [
        control_id,
        control_name,
        control_type,
        framework,
        owner,
        status,
        description
    ]

    with open(CONTROL_FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(control)

    print("Control added successfully.")


def view_controls():

    controls = []

    with open(CONTROL_FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            controls.append(row)

    print("\n========== Controls Library ==========")

    if not controls:
        print("No controls found.")
        return

    for row in controls:
        print("--------------------------------------")
        print(f"Control ID:    {row[0]}")
        print(f"Control Name:  {row[1]}")
        print(f"Type:          {row[2]}")
        print(f"Framework:     {row[3]}")
        print(f"Owner:         {row[4]}")
        print(f"Status:        {row[5]}")
        print(f"Description:   {row[6]}")


def link_control_to_risk():
    print("\n========== Link Control to Risk ==========")

    risk_id = input("Enter Risk ID: ").strip().upper()
    control_id = input("Enter Control ID: ").strip().upper()

    mapping = [
        risk_id,
        control_id
    ]

    with open(MAPPING_FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(mapping)

    print(f"Linked {control_id} to {risk_id} successfully.")


def view_controls_for_risk():
    risk_id = input("\nEnter Risk ID: ").strip().upper()

    linked_control_ids = []

    with open(MAPPING_FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue

            if row[0].strip().upper() == risk_id:
                linked_control_ids.append(row[1].strip().upper())

    if not linked_control_ids:
        print("No controls linked to this risk.")
        return

    print(f"\n========== Controls for {risk_id} ==========")

    with open(CONTROL_FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue

            if row[0].strip().upper() in linked_control_ids:
                print("--------------------------------------")
                print(f"Control ID:    {row[0]}")
                print(f"Control Name:  {row[1]}")
                print(f"Type:          {row[2]}")
                print(f"Framework:     {row[3]}")
                print(f"Owner:         {row[4]}")
                print(f"Status:        {row[5]}")
                print(f"Description:   {row[6]}")
                

def get_controls_for_risk(risk_id):

    linked_controls = []

    linked_control_ids = []

    with open(MAPPING_FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue

            if row[0].strip().upper() == risk_id.upper():
                linked_control_ids.append(row[1].strip().upper())

    with open(CONTROL_FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue

            if row[0].strip().upper() in linked_control_ids:
                linked_controls.append(row)

    return linked_controls


def controls_menu():
    create_control_file_if_missing()
    create_mapping_file_if_missing()

    while True:
        print("\n========== Controls Library ==========")
        print("1. Add Control")
        print("2. View Controls")
        print("3. Link Control to Risk")
        print("4. View Controls for a Risk")
        print("5. Return to Main Menu")
        print("======================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_control()
        elif choice == "2":
            view_controls()
        elif choice == "3":
            link_control_to_risk()
        elif choice == "4":
            view_controls_for_risk()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")