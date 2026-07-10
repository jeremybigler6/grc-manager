import csv
import os
from datetime import date, datetime
from pathlib import Path

from framework_ai_lookup import explain_framework_control
from controls import get_controls_for_selection, display_controls_for_selection
from openai_helper import ask_openai


PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"
RISKS_FILE = DATA_FOLDER / "risk_register.csv"
CONTROLS_FILE = DATA_FOLDER / "controls_library.csv"
MAPPING_FILE = DATA_FOLDER / "risk_control_mapping.csv"
POLICY_FOLDER = PROJECT_FOLDER / "generated_policies"
REPORT_FOLDER = PROJECT_FOLDER / "generated_reports"


def ai_risk_advisor_menu(risk=None):
    print("\n========== AI Risk Advisor ==========")

    if risk:
        scenario = f"""
Risk ID: {risk[0]}
Risk Name: {risk[1]}
Category: {risk[2]}
Likelihood: {risk[3]}
Impact: {risk[4]}
Risk Score: {risk[5]}
Risk Level: {risk[6]}
Owner: {risk[7]}
Treatment Plan: {risk[8]}
Status: {risk[9]}
"""
    else:
        scenario = input("Describe the business or cybersecurity scenario: ")

    system_prompt = "You are a cybersecurity GRC analyst. Provide a concise, practical risk analysis with clear actions."
    user_prompt = f"Analyze this scenario and give a short structured response.\n\n{scenario}"
    ai_result = ask_openai(system_prompt, user_prompt)

    result = ai_result.strip() if ai_result else None
    if not result:
        result = (
            "Fallback risk analysis:\n"
            "- Review the scenario for control gaps and ownership issues.\n"
            "- Highlight likely risk drivers, likely impact, and next-step mitigation actions."
        )

    print("\n========== AI Risk Analysis ==========")
    print(result)


def adhoc_framework_workspace():
    print("\n========== 🛠️ Ad-Hoc AI Workspace: Framework Architecture ==========")
    print("1. ISO 27001")
    print("2. NIST CSF")
    print("3. SOC 2")
    print("4. PCI DSS")
    print("5. Custom Framework")

    choice = input("Choose a framework (1-5): ").strip()

    if choice == "1":
        framework = "ISO 27001"
    elif choice == "2":
        framework = "NIST CSF"
    elif choice == "3":
        framework = "SOC 2"
    elif choice == "4":
        framework = "PCI DSS"
    elif choice == "5":
        framework = input("Framework name: ").strip()
    else:
        print("Invalid choice.")
        return

    print(f"\n--- {framework} Architecture Workbench ---")
    # Instead of asking for a Control ID, we ask for any index, section, or structural code
    structure_query = input("Enter a section code, index, or clause (e.g., 'A.5', 'PR.AC', '3.a.5'): ").strip()
    
    if not structure_query:
        print("No structural query entered.")
        return

    # This prompt instructs the AI to identify the structural taxonomy first
    system_prompt = (
        "You are an expert cybersecurity GRC architect. Your job is to parse framework references "
        "and identify what those structural elements are called in their respective taxonomies "
        "(e.g., Functions, Categories, Subcategories, Clauses, Domains, or Requirements). "
        "Explain what the component is called, where it fits in the framework hierarchy, "
        "and its GRC objective in plain English."
    )
    
    user_prompt = f"""
    Analyze the following reference within the specified compliance framework:
    Framework: {framework}
    Reference Code/Query: {structure_query}
    
    Provide a breakdown that includes:
    1. What this structural tier or notation is called in this framework (e.g., 'Subcategory', 'Annex A Control Domain', 'Trust Services Criteria Category').
    2. Where it sits in the overall hierarchy.
    3. A plain English translation of what it covers and why it matters to an auditor.
    """

    print(f"\n[AI Workspace] Mapping architecture for {framework} reference '{structure_query}'...")
    ai_result = ask_openai(system_prompt, user_prompt)

    result = ai_result.strip() if ai_result else None
    if not result:
        result = f"Unable to map structural details for {framework} reference {structure_query}."

    print("\n================ 📋 Structural Taxonomy Report ================")
    print(result)
    print("===============================================================")


def load_csv_rows(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append_csv_row(file_path, row):
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if not file_exists:
            if file_path == CONTROLS_FILE:
                writer.writerow(["Control ID", "Control Name", "Control Type", "Framework", "Owner", "Status", "Description"])
            elif file_path == MAPPING_FILE:
                writer.writerow(["Risk ID", "Control ID"])
        writer.writerow(row)


def get_risk_by_id(risk_id):
    risks = load_csv_rows(RISKS_FILE)
    for risk in risks:
        if risk.get("Risk ID", "").strip().upper() == risk_id.strip().upper():
            return risk
    return None


def get_control_by_id(control_id):
    controls = load_csv_rows(CONTROLS_FILE)
    for control in controls:
        if control.get("Control ID", "").strip().upper() == control_id.strip().upper():
            return control
    return None


def get_next_control_id():
    controls = load_csv_rows(CONTROLS_FILE)
    ids = []

    for control in controls:
        control_id = control.get("Control ID", "")
        if control_id.startswith("C-"):
            try:
                ids.append(int(control_id.split("-")[-1]))
            except ValueError:
                continue

    if not ids:
        return "C-001"

    next_number = max(ids) + 1
    return f"C-{next_number:03d}"


def generate_control_suggestion(risk_row, control_type):
    risk_name = risk_row.get("Risk Name", "Unknown Risk")
    category = risk_row.get("Category", "").lower()
    owner = risk_row.get("Owner", "Operations")

    if any(word in category for word in ["safety", "operations", "maintenance", "environment", "hazard", "permit", "turbine"]):
        base_name = "Operational Verification Procedure"
        framework = "Internal Operational Control"
        description = (
            f"Designed for {risk_name} and aligned to the {risk_row.get('Category', 'risk')} risk area. "
            f"This control requires routine inspections, documented checks, and clear escalation steps."
        )
    elif any(word in category for word in ["cyber", "access", "data", "governance", "incident", "vendor", "compliance"]):
        base_name = "Security and Compliance Control"
        framework = "NIST CSF"
        description = (
            f"Designed for {risk_name} and aligned to the {risk_row.get('Category', 'risk')} risk area. "
            f"This control supports monitoring, evidence collection, and periodic review."
        )
    else:
        base_name = "Risk Mitigation Control"
        framework = "Internal Control"
        description = (
            f"Designed for {risk_name} and aligned to the {risk_row.get('Category', 'risk')} risk area. "
            f"This control should be reviewed for ownership, evidence, and recurring execution."
        )

    if control_type == "Preventive":
        name = f"Preventive {base_name}"
        description = description + " It is intended to reduce the chance of the risk occurring."
    elif control_type == "Detective":
        name = f"Detective {base_name}"
        description = description + " It is intended to detect issues early and trigger follow-up action."
    else:
        name = f"Corrective {base_name}"
        description = description + " It is intended to respond after an issue occurs and restore control."

    return {
        "name": name,
        "control_type": control_type,
        "framework": framework,
        "owner": owner,
        "description": description,
        "status": "Proposed"
    }


def control_builder_menu():
    print("\n========== Control Builder ==========")

    risk_id = input("Enter Risk ID: ").strip().upper()
    risk = get_risk_by_id(risk_id)

    if not risk:
        print("Risk not found.")
        return

    print("\nSelected Risk")
    print("-" * 40)
    print(f"Risk ID:      {risk.get('Risk ID', '')}")
    print(f"Risk Name:    {risk.get('Risk Name', '')}")
    print(f"Category:     {risk.get('Category', '')}")
    print(f"Risk Level:   {risk.get('Risk Level', '')}")
    print(f"Owner:        {risk.get('Owner', '')}")

    print("\nChoose a control type:")
    print("1. Preventive")
    print("2. Detective")
    print("3. Corrective")

    control_choice = input("\nSelect an option: ").strip()

    if control_choice == "1":
        control_type = "Preventive"
    elif control_choice == "2":
        control_type = "Detective"
    elif control_choice == "3":
        control_type = "Corrective"
    else:
        print("Invalid choice.")
        return

    suggestion = generate_control_suggestion(risk, control_type)

    system_prompt = "You are a cybersecurity GRC analyst. Suggest a concise control recommendation for the given risk."
    user_prompt = (
        f"Create a short control recommendation for this risk. "
        f"Risk Name: {risk.get('Risk Name', '')}; Category: {risk.get('Category', '')}; "
        f"Control Type: {control_type}; Owner: {risk.get('Owner', '')}."
    )
    ai_result = ask_openai(system_prompt, user_prompt)

    if ai_result and ai_result.strip():
        print("\nOpenAI-enhanced Control Recommendation")
        print("-" * 40)
        print(ai_result.strip())
    else:
        print("\nSuggested Control")
        print("-" * 40)
        print(f"Control Name: {suggestion['name']}")
        print(f"Type:         {suggestion['control_type']}")
        print(f"Framework:    {suggestion['framework']}")
        print(f"Owner:        {suggestion['owner']}")
        print(f"Description:  {suggestion['description']}")

    save_choice = input("\nSave this control to the library? (y/n): ").strip().lower()
    if save_choice not in ["y", "yes"]:
        print("Control not saved.")
        return

    new_control_id = get_next_control_id()
    new_control_row = [
        new_control_id,
        suggestion["name"],
        suggestion["control_type"],
        suggestion["framework"],
        suggestion["owner"],
        suggestion["status"],
        suggestion["description"],
    ]

    append_csv_row(CONTROLS_FILE, new_control_row)
    append_csv_row(MAPPING_FILE, [risk_id, new_control_id])

    print(f"\nControl saved as {new_control_id}.")
    print(f"Mapping added for Risk {risk_id}.")


def generate_policy_text(risk_row):
    risk_name = risk_row.get("Risk Name", "Unknown Risk")
    category = risk_row.get("Category", "").lower()

    if any(word in category for word in ["safety", "operations", "maintenance", "environment", "hazard", "permit", "turbine"]):
        return f"""Operational Procedure
====================
Risk: {risk_name}
Purpose: Maintain safe and reliable operations for this risk area.

Requirements:
1. Assign an accountable owner for the process.
2. Perform routine checks and documented inspections.
3. Record evidence of completion and review results.
4. Escalate deviations to management and follow up on corrective action.

Review Cycle: Quarterly or after significant incidents.
"""

    return f"""Security and Compliance Policy
=============================
Risk: {risk_name}
Purpose: Establish clear expectations for managing this control and supporting evidence.

Requirements:
1. Assign an accountable owner.
2. Maintain documented procedures and review cadence.
3. Collect evidence of execution and periodic review.
4. Report gaps and remediation actions to management.

Review Cycle: Quarterly or after major control changes.
"""


def policy_generator_menu():
    print("\n========== Policy Generator ==========")

    risk_id = input("Enter Risk ID: ").strip().upper()
    risk = get_risk_by_id(risk_id)

    if not risk:
        print("Risk not found.")
        return

    print("\nSelected Risk")
    print("-" * 40)
    print(f"Risk ID:    {risk.get('Risk ID', '')}")
    print(f"Risk Name:  {risk.get('Risk Name', '')}")
    print(f"Category:   {risk.get('Category', '')}")

    policy_text = generate_policy_text(risk)

    system_prompt = "You are a cybersecurity GRC analyst. Draft a concise policy for the given risk with clear requirements."
    user_prompt = f"Draft a short policy for this risk. Risk Name: {risk.get('Risk Name', '')}; Category: {risk.get('Category', '')}."
    ai_result = ask_openai(system_prompt, user_prompt)
    if ai_result and ai_result.strip():
        policy_text = ai_result.strip()

    print("\nGenerated Policy")
    print("-" * 40)
    print(policy_text)

    save_choice = input("\nSave this policy to a file? (y/n): ").strip().lower()
    if save_choice not in ["y", "yes"]:
        print("Policy not saved.")
        return

    POLICY_FOLDER.mkdir(exist_ok=True)
    file_name = f"{risk_id.lower()}_policy.txt"
    file_path = POLICY_FOLDER / file_name

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(policy_text)

    print(f"Policy saved to {file_path}")


def review_evidence(control_row, evidence_text):
    text = f"{control_row.get('Control Name', '')} {control_row.get('Description', '')} {evidence_text}".lower()

    if any(word in text for word in ["approval", "review", "test", "log", "evidence", "report", "record", "ticket", "audit", "monitor"]):
        if any(word in text for word in ["approval", "review", "audit", "record", "report", "ticket"]):
            support_level = "Yes"
            missing = "No major gaps identified."
        else:
            support_level = "Partial"
            missing = "Add a dated review record or approval artifact."
    else:
        support_level = "No"
        missing = "Add a clear artifact such as a screenshot, approval, log, or review record."

    if support_level == "Yes":
        next_evidence = "Keep the current evidence and add a periodic review record."
    elif support_level == "Partial":
        next_evidence = "Add a signed review or test record to strengthen the evidence."
    else:
        next_evidence = "Add an execution log, approval, or documented review artifact."

    return support_level, missing, next_evidence


def evidence_review_menu():
    print("\n========== Evidence Review ==========")

    control_id = input("Enter Control ID: ").strip().upper()
    control = get_control_by_id(control_id)

    if not control:
        print("Control not found.")
        return

    print("\nSelected Control")
    print("-" * 40)
    print(f"Control ID:   {control.get('Control ID', '')}")
    print(f"Control Name: {control.get('Control Name', '')}")
    print(f"Type:         {control.get('Control Type', '')}")
    print(f"Framework:    {control.get('Framework', '')}")
    print(f"Description:  {control.get('Description', '')}")

    evidence_text = input("\nPaste a short evidence description: ").strip()
    support_level, missing, next_evidence = review_evidence(control, evidence_text)

    system_prompt = "You are a cybersecurity GRC analyst. Review evidence and provide a concise assessment of control support."
    user_prompt = (
        f"Review this evidence for a control. Control: {control.get('Control Name', '')}; "
        f"Description: {control.get('Description', '')}; Evidence: {evidence_text}."
    )
    ai_result = ask_openai(system_prompt, user_prompt)

    print("\nEvidence Review")
    print("-" * 40)
    if ai_result and ai_result.strip():
        print(ai_result.strip())
    else:
        print(f"Control being reviewed: {control.get('Control ID', '')} - {control.get('Control Name', '')}")
        print(f"Evidence summary: {evidence_text}")
        print(f"Does it support the control? {support_level}")
        print(f"What is missing: {missing}")
        print(f"Recommended next evidence: {next_evidence}")


def build_risk_report_text():
    risks = load_csv_rows(RISKS_FILE)
    total_risks = len(risks)
    open_risks = sum(1 for row in risks if row.get("Status", "").strip().lower() == "open")
    closed_risks = sum(1 for row in risks if row.get("Status", "").strip().lower() == "closed")
    high_critical = sum(1 for row in risks if row.get("Risk Level", "").strip().lower() in ["high", "critical"])

    top_risks = sorted(risks, key=lambda row: int(row.get("Risk Score", 0) or 0), reverse=True)[:5]

    categories = {}
    for row in risks:
        category = row.get("Category", "Uncategorized")
        categories[category] = categories.get(category, 0) + 1

    today = date.today()
    overdue_risks = []
    for row in risks:
        if row.get("Status", "").strip().lower() == "closed":
            continue

        target_date = row.get("Target Date", "")
        try:
            target_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            continue

        if target_dt < today:
            overdue_risks.append(row)

    lines = []
    lines.append("Risk Report")
    lines.append("=" * 40)
    lines.append(f"Total Risks: {total_risks}")
    lines.append(f"Open Risks: {open_risks}")
    lines.append(f"Closed Risks: {closed_risks}")
    lines.append(f"High/Critical Risks: {high_critical}")
    lines.append("")
    lines.append("Top 5 Risks by Risk Score")
    lines.append("-" * 40)
    for row in top_risks:
        lines.append(f"{row.get('Risk ID', '')} | {row.get('Risk Name', '')} | Score: {row.get('Risk Score', '')} | Level: {row.get('Risk Level', '')}")

    lines.append("")
    lines.append("Risks by Category")
    lines.append("-" * 40)
    for category, count in sorted(categories.items()):
        lines.append(f"{category}: {count}")

    lines.append("")
    lines.append("Overdue Risks")
    lines.append("-" * 40)
    if overdue_risks:
        for row in overdue_risks:
            lines.append(f"{row.get('Risk ID', '')} | {row.get('Risk Name', '')} | Due: {row.get('Target Date', '')}")
    else:
        lines.append("No overdue risks found.")

    return "\n".join(lines)


def report_writer_menu():
    print("\n========== Report Writer ==========")
    report_text = build_risk_report_text()

    system_prompt = "You are a cybersecurity GRC analyst. Summarize risk data in a concise report format."
    user_prompt = f"Create a concise risk report summary from this data.\n\n{report_text}"
    ai_result = ask_openai(system_prompt, user_prompt)
    if ai_result and ai_result.strip():
        report_text = ai_result.strip()

    print(report_text)

    save_choice = input("\nSave this report to a file? (y/n): ").strip().lower()
    if save_choice not in ["y", "yes"]:
        print("Report not saved.")
        return

    REPORT_FOLDER.mkdir(exist_ok=True)
    file_path = REPORT_FOLDER / "risk_report.txt"

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(report_text)

    print(f"Report saved to {file_path}")


def ai_tools_menu(risk=None):
    while True:
        print("\n========== AI Ad-Hoc Workspace ==========")

        if risk:
            print(f"Working with Risk: {risk[0]} - {risk[1]}")

        print("1. AI Risk Advisor")
        print("2. Framework Assistant")
        print("B. Back")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            ai_risk_advisor_menu(risk)

        elif choice == "2":
            print("\n========== Framework Assistant ==========")
            framework = input("Framework name: ").strip()
            control_id = input("Control ID: ").strip()
            if framework and control_id:
                try:
                    print(explain_framework_control(framework, control_id))
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Cannot be empty.")

        elif choice.upper() == "B":
            break

        else:
            print("Invalid choice.")