from database import connect_db


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

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO controls
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, control)

    conn.commit()
    conn.close()

    print("Control added successfully.")


def view_controls():

    controls = []

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM controls")
    controls = cursor.fetchall()

    conn.close()

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

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO risk_control_mapping
        VALUES (?, ?)
    """, (risk_id, control_id))

    conn.commit()
    conn.close()

    print(f"Linked {control_id} to {risk_id} successfully.")


def view_controls_for_risk():
    risk_id = input("\nEnter Risk ID: ").strip().upper()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT controls.*
        FROM controls
        JOIN risk_control_mapping
        ON controls.control_id = risk_control_mapping.control_id
        WHERE risk_control_mapping.risk_id = ?
    """, (risk_id,))

    controls = cursor.fetchall()

    conn.close()

    if not controls:
        print("No controls linked to this risk.")
        return

    print(f"\n========== Controls for {risk_id} ==========")

    for row in controls:
        print("--------------------------------------")
        print(f"Control ID:    {row[0]}")
        print(f"Control Name:  {row[1]}")
        print(f"Type:          {row[2]}")
        print(f"Framework:     {row[3]}")
        print(f"Owner:         {row[4]}")
        print(f"Status:        {row[5]}")
        print(f"Description:   {row[6]}")
                

def get_controls_for_risk(risk_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT controls.*
        FROM controls
        JOIN risk_control_mapping
        ON controls.control_id = risk_control_mapping.control_id
        WHERE risk_control_mapping.risk_id = ?
    """, (risk_id.upper(),))

    linked_controls = cursor.fetchall()

    conn.close()

    return linked_controls


def controls_menu():

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