from database import connect_db
from audit_trail import log_activity


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

    log_activity("Control Added", f"{control_id} - {control_name}")
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


def get_risks_for_selection(search_term=None):
    conn = connect_db()
    cursor = conn.cursor()

    if search_term:
        cursor.execute("""
            SELECT risk_id, risk_name, category, status, risk_level
            FROM risks
            WHERE lower(risk_id) LIKE ?
               OR lower(risk_name) LIKE ?
               OR lower(category) LIKE ?
            ORDER BY risk_id
        """, (f"%{search_term.lower()}%", f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
    else:
        cursor.execute("""
            SELECT risk_id, risk_name, category, status, risk_level
            FROM risks
            ORDER BY risk_id
        """)

    risks = cursor.fetchall()
    conn.close()
    return risks


def get_controls_for_selection(search_term=None):
    conn = connect_db()
    cursor = conn.cursor()

    if search_term:
        cursor.execute("""
            SELECT control_id, control_name, control_type, framework, owner, status
            FROM controls
            WHERE lower(control_id) LIKE ?
               OR lower(control_name) LIKE ?
               OR lower(framework) LIKE ?
            ORDER BY control_id
        """, (f"%{search_term.lower()}%", f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
    else:
        cursor.execute("""
            SELECT control_id, control_name, control_type, framework, owner, status
            FROM controls
            ORDER BY control_id
        """)

    controls = cursor.fetchall()
    conn.close()
    return controls


def display_risks_for_selection(risks, title):
    print(f"\n========== {title} ==========")

    if not risks:
        print("No risks found.")
        return []

    for index, risk in enumerate(risks, start=1):
        risk_id, risk_name, category, status, risk_level = risk
        print(f"{index}. {risk_id} - {risk_name}")
        print(f"   Category: {category} | Status: {status} | Level: {risk_level}")

    return risks


def select_risk_from_list():
    while True:
        print("\n========== Select a Risk ==========")
        print("1. Browse all risks")
        print("2. Search risks by keyword")
        print("3. Return")
        print("====================================")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            risks = get_risks_for_selection()
            displayed = display_risks_for_selection(risks, "Available Risks")
            if not displayed:
                continue

            selection = input("\nChoose a risk number to continue (or press Enter to go back): ").strip()
            if not selection:
                continue

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(displayed):
                    return displayed[index]
                print("Invalid selection.")
            else:
                print("Please enter a number.")

        elif choice == "2":
            search_term = input("Enter a risk ID, name, or category: ").strip()
            if not search_term:
                print("No search term entered.")
                continue

            risks = get_risks_for_selection(search_term)
            displayed = display_risks_for_selection(risks, f"Search Results for '{search_term}'")
            if not displayed:
                continue

            selection = input("\nChoose a risk number to continue (or press Enter to go back): ").strip()
            if not selection:
                continue

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(displayed):
                    return displayed[index]
                print("Invalid selection.")
            else:
                print("Please enter a number.")

        elif choice == "3":
            return None

        else:
            print("Invalid choice. Try again.")


def display_controls_for_selection(controls, title):
    print(f"\n========== {title} ==========")

    if not controls:
        print("No controls found.")
        return []

    for index, control in enumerate(controls, start=1):
        control_id, control_name, control_type, framework, owner, status = control
        print(f"{index}. {control_id} - {control_name}")
        print(f"   Type: {control_type} | Framework: {framework} | Owner: {owner} | Status: {status}")

    return controls


def select_control_from_list():
    while True:
        print("\n========== Select a Control ==========")
        print("1. Browse all controls")
        print("2. Search controls by keyword")
        print("3. Return")
        print("====================================")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            controls = get_controls_for_selection()
            displayed = display_controls_for_selection(controls, "Available Controls")
            if not displayed:
                continue

            selection = input("\nChoose a control number to continue (or press Enter to go back): ").strip()
            if not selection:
                continue

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(displayed):
                    return displayed[index]
                print("Invalid selection.")
            else:
                print("Please enter a number.")

        elif choice == "2":
            search_term = input("Enter a control ID, name, or framework: ").strip()
            if not search_term:
                print("No search term entered.")
                continue

            controls = get_controls_for_selection(search_term)
            displayed = display_controls_for_selection(controls, f"Search Results for '{search_term}'")
            if not displayed:
                continue

            selection = input("\nChoose a control number to continue (or press Enter to go back): ").strip()
            if not selection:
                continue

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(displayed):
                    return displayed[index]
                print("Invalid selection.")
            else:
                print("Please enter a number.")

        elif choice == "3":
            return None

        else:
            print("Invalid choice. Try again.")


def control_exists(control_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM controls WHERE control_id = ?", (control_id.upper(),))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def link_control_to_risk():
    print("\n========== Link Control to Risk ==========")

    selected_risk = select_risk_from_list()
    if not selected_risk:
        print("No risk selected.")
        return

    risk_id = selected_risk[0]
    print(f"\nSelected risk: {risk_id} - {selected_risk[1]}")

    selected_control = select_control_from_list()
    if not selected_control:
        print("No control selected.")
        return

    control_id = selected_control[0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM risk_control_mapping
        WHERE risk_id = ? AND control_id = ?
    """, (risk_id, control_id))

    if cursor.fetchone():
        conn.close()
        print(f"{control_id} is already linked to {risk_id}.")
        return

    cursor.execute("""
        INSERT INTO risk_control_mapping
        VALUES (?, ?)
    """, (risk_id, control_id))

    conn.commit()
    conn.close()

    log_activity("Control Linked", f"{risk_id} ↔ {control_id}")
    print(f"Linked {control_id} to {risk_id} successfully.")


def view_controls_for_risk():
    print("\n========== View Controls for a Risk ==========")

    selected_risk = select_risk_from_list()
    if not selected_risk:
        print("No risk selected.")
        return

    risk_id = selected_risk[0]

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
        print(f"No controls linked to {risk_id}.")
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


def view_all_risks_with_controls():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT risk_id, risk_name, category, status, risk_level
        FROM risks
        ORDER BY risk_id
    """)

    risks = cursor.fetchall()
    conn.close()

    print("\n========== Risks and Associated Controls ==========")

    if not risks:
        print("No risks found.")
        return

    for risk in risks:
        risk_id, risk_name, category, status, risk_level = risk
        print(f"\n{risk_id} - {risk_name}")
        print(f"Category: {category} | Status: {status} | Level: {risk_level}")

        controls = get_controls_for_risk(risk_id)
        if not controls:
            print("   No controls linked.")
            continue

        print("   Linked Controls:")
        for control in controls:
            print(f"   - {control[0]} | {control[1]}")


def controls_menu():

    while True:
        print("\n========== Controls Library ==========")
        print("1. Add Control")
        print("2. View Controls")
        print("3. Browse/Search Risks")
        print("4. Link Control to Risk")
        print("5. View Controls for a Risk")
        print("6. Risk-Control Coverage Report")
        print("B. Return to Main Menu")
        print("======================================")

        choice = input("\nSelect an option: ").strip().upper()

        if choice == "1":
            add_control()
        elif choice == "2":
            view_controls()
        elif choice == "3":
            selected_risk = select_risk_from_list()
            if selected_risk:
                print(f"\nSelected risk: {selected_risk[0]} - {selected_risk[1]}")
        elif choice == "4":
            link_control_to_risk()
        elif choice == "5":
            view_controls_for_risk()
        elif choice == "6":
            view_all_risks_with_controls()
        elif choice == "B":
            break
        else:
            print("Invalid choice. Try again.")