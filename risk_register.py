from datetime import date
from controls import get_controls_for_risk
from database import connect_db


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

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO risks
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, risk)

    conn.commit()
    conn.close()

    print(f"\nRisk added successfully. Risk Level: {risk_level}")


def view_risks():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM risks")

    risks = cursor.fetchall()

    conn.close()

    if not risks:
        print("\nNo risks found.")
        return

    display_risks("Risk Register", risks)
    

def edit_risk():
    risk_id = input("\nEnter Risk ID to edit: ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE risk_id = ?
    """, (risk_id,))

    risk = cursor.fetchone()

    if not risk:
        print("\nRisk not found.")
        conn.close()
        return

    print("\nLeave blank to keep the current value.\n")

    risk_name = input(f"Risk Name [{risk[1]}]: ") or risk[1]
    category = input(f"Category [{risk[2]}]: ") or risk[2]

    likelihood_input = input(f"Likelihood [{risk[3]}]: ")
    likelihood = int(likelihood_input) if likelihood_input else risk[3]

    impact_input = input(f"Impact [{risk[4]}]: ")
    impact = int(impact_input) if impact_input else risk[4]

    risk_score = likelihood * impact
    risk_level = calculate_risk_level(risk_score)

    owner = input(f"Owner [{risk[7]}]: ") or risk[7]
    treatment_plan = input(f"Treatment Plan [{risk[8]}]: ") or risk[8]
    status = input(f"Status [{risk[9]}]: ") or risk[9]
    target_date = input(f"Target Date [{risk[12]}]: ") or risk[12]

    today = date.today().isoformat()

    cursor.execute("""
        UPDATE risks
        SET risk_name = ?,
            category = ?,
            likelihood = ?,
            impact = ?,
            risk_score = ?,
            risk_level = ?,
            owner = ?,
            treatment_plan = ?,
            status = ?,
            last_review_date = ?,
            target_date = ?
        WHERE risk_id = ?
    """, (
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
        target_date,
        risk_id
    ))

    conn.commit()
    conn.close()

    print("\nRisk updated successfully.")


def delete_risk():
    risk_id = input("\nEnter Risk ID to delete: ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM risks
        WHERE risk_id = ?
    """, (risk_id,))

    conn.commit()
    conn.close()

    print(f"\nRisk {risk_id} deleted successfully.")


def view_risk_details():

    risk_id = input("Enter Risk ID: ").strip().upper()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE risk_id = ?
    """, (risk_id,))

    risk = cursor.fetchone()

    if not risk:
        print("Risk not found.")
        conn.close()
        return

    print("\n========== Risk Details ==========\n")

    print(f"Risk ID:         {risk[0]}")
    print(f"Risk Name:       {risk[1]}")
    print(f"Category:        {risk[2]}")

    print()

    print(f"Likelihood:      {risk[3]}")
    print(f"Impact:          {risk[4]}")
    print(f"Risk Score:      {risk[5]}")
    print(f"Risk Level:      {risk[6]}")

    print()

    print(f"Owner:           {risk[7]}")
    print(f"Status:          {risk[9]}")

    print()

    print(f"Date Created:    {risk[10]}")
    print(f"Last Updated:    {risk[11]}")
    print(f"Completion Date: {risk[12]}")

    print()

    print("Treatment Plan")
    print("-" * 40)
    print(risk[8])

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
    search_term = input("\nEnter search term: ").strip().lower()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE lower(risk_id) LIKE ?
           OR lower(risk_name) LIKE ?
           OR lower(category) LIKE ?
           OR lower(owner) LIKE ?
           OR lower(status) LIKE ?
    """, (
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%",
        f"%{search_term}%"
    ))

    risks = cursor.fetchall()
    conn.close()

    if not risks:
        print("\nNo matching risks found.")
        return

    display_risks("Search Results", risks)


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

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM risks")
    risks = cursor.fetchall()

    conn.close()

    for row in risks:

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

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM risks")

    risks = cursor.fetchall()

    conn.close()

    for row in risks:
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

    today = date.today().isoformat()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE status != 'Closed'
    """)

    risks = cursor.fetchall()

    conn.close()

    upcoming_risks = []

    for row in risks:
        target_date = date.fromisoformat(row[12])
        days_until_due = (target_date - date.today()).days

        if 0 <= days_until_due <= 7:
            upcoming_risks.append(row)

    display_risks("Due Soon Risks", upcoming_risks)



def view_overdue_risks():

    today = date.today().isoformat()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE status != 'Closed'
        AND completion_date < ?
    """, (today,))

    overdue_risks = cursor.fetchall()

    conn.close()

    display_risks("Overdue Risks", overdue_risks)


def view_critical_risks():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM risks
        WHERE risk_level = 'Critical'
    """)

    critical_risks = cursor.fetchall()

    conn.close()

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