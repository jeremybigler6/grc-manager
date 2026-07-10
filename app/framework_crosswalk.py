import sqlite3
import json
from openai import OpenAI


def fetch_ai_crosswalk_suggestions(control_title, control_desc):
    client = OpenAI() # intialize the obejct for the OpenAI API client
    system_prompt = """
    You are an expert IT compliance auditor and GRC analyst. Analyze the provided Internal Control and suggest the most accurate mappings for:
    1. NIST CSF v2.0
    2. ISO/IEC 27001:2022
    3. AICPA SOC 2 Trust Services Criteria (2017)

    Your response must be a valid, raw JSON object containing a "mappings" array. Do not include markdown code block syntax.

    CRITICAL CONFIDENCE SCORING RULES:
    Calculate the "confidence_score" using this strict mathematical rubric:
    - NEVER score a control based on its Title. You must grade the score SOLELY on the execution details provided in the Description. If the description describes an unencrypted, manual, or unverified process, it CANNOT be higher than 0.5.
    - 1.0 (Direct Match): The internal control explicitly implements the exact requirement named in the framework clause.
    - 0.8 (Strong Alignment): The control satisfies the core intent of the clause, but uses slightly different operational mechanisms.
    - 0.5 (Partial Match): The control provides secondary evidence but leaves a clear gap.

    Each object in the "mappings" array must have these exact keys and types:
    - "framework_name": String ('NIST CSF', 'ISO 27001', or 'SOC 2')
    - "suggested_section_id": String (e.g., 'PR.MA-01', 'A.8.14', 'CC7.1')
    - "confidence_score": Float
    - "ai_rationale": String (Must follow this exact 3-part template:
       1. FRAMEWORK CLAUSE: [State exactly what requirement or control objective this framework section mandates].
       2. CONTROL ANALYSIS: [Identify what specific keywords or mechanisms from the user's control align with or fail this requirement].
       3. THE BRIDGE: [Explain exactly how this control bridges the risk gap, or explicitly detail what specific operational steps are missing to escalate this from a 0.5 to a 1.0 match].)
    """
    # The user prompt passes the dynamic data for this specific run
    user_prompt = f"""
    Analyze the following internal control:
    Title: {control_title}
    Description: {control_desc}
    """


    try:  #exeption handling for API call and JSON parsing
        # Call the OpenAI API using the latest SDK syntax. Sub folders to .create(). .create() triggers HTTP network request, bundles the prompts and fires them ato the OpenAI API endpoint. The response is a JSON object containing the model's output.
        response = client.chat.completions.create(
            model="gpt-4o",  # Or your preferred model like gpt-4-turbo
            response_format={"type": "json_object"},  # Guarantees the output is a valid JSON object
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2  # Low temperature keeps the mapping logical and deterministic. Avoiding hallucinations is critical for compliance mapping tasks.
        )
        
        # Extract the raw text string from the response
        raw_json_output = response.choices[0].message.content
        
        # Parse the string into a Python dictionary
        # import json
        parsed_data = json.loads(raw_json_output)
        
        # Return just the array of mappings to make database ingestion easier
        return parsed_data.get("mappings", [])

    except Exception as e:
        print(f"Error fetching AI crosswalk suggestions: {e}")
        return []
        

def init_crosswalk_tables(db_path="grc_manager.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS internal_controls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        control_id TEXT UNIQUE,
        title TEXT,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_mapping_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internal_control_id INTEGER,
        framework_name TEXT,
        suggested_section_id TEXT,
        confidence_score REAL,
        ai_rationale TEXT,
        status TEXT DEFAULT 'PENDING',
        FOREIGN KEY(internal_control_id) REFERENCES internal_controls(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS framework_mappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internal_control_id INTEGER,
        framework_name TEXT,
        framework_section_id TEXT,
        mapping_rationale TEXT,
        FOREIGN KEY(internal_control_id) REFERENCES internal_controls(id)
    );
    """)
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS control_risk_links (
        internal_control_id INTEGER,
        risk_id TEXT,
        PRIMARY KEY (internal_control_id, risk_id)
    );
    """)

    conn.commit()
    conn.close()    


def add_internal_control(control_id, title, description, db_path="grc_manager.db"):
    """Inserts a new internal control and returns its database integer ID."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO internal_controls (control_id, title, description)
            VALUES (?, ?, ?);
        """, (control_id, title, description))
        conn.commit()
        # lastrowid grabs the auto-incremented integer 'id' of the row we just inserted
        inserted_id = cursor.lastrowid
        return inserted_id
    except sqlite3.IntegrityError:
        # Handles the case where CTRL-101 already exists in your table
        cursor.execute("SELECT id FROM internal_controls WHERE control_id = ?;", (control_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def process_control_crosswalk(internal_control_db_id, db_path="grc_manager.db"):
    """Fetches a control, generates AI suggestions, lets the analyst filter them,

    and sends approved items to the manager review queue as PENDING.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, description FROM internal_controls WHERE id = ?;
    """, (internal_control_db_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"Control ID {internal_control_db_id} not found in database.")
        conn.close()
        return

    control_title, control_desc = row

    print(f"\nAnalyzing control: {control_title}")
    suggestions = fetch_ai_crosswalk_suggestions(control_title, control_desc)
    
    if not suggestions:
        print("No framework mappings suggested by AI.")
        conn.close()
        return

    print(f"\n--- AI SUGGESTED MAPPINGS FOUND ({len(suggestions)}) ---")
    
    # Display options with numbers
    for idx, mapping in enumerate(suggestions, 1):
        print(f"\n[{idx}] Framework: {mapping.get('framework_name')}")
        print(f"    Agent's Control Adequacy Rating: {mapping.get('confidence_score')}")
        print(f"    Section ID: {mapping.get('suggested_section_id')}")
        print(f"    Rationale:  {mapping.get('ai_rationale')}")
    print("-" * 50)

    # Multi-choice prompt selection for initial analyst filtering
    print("Options: Enter 'all', 'none', or specific numbers separated by commas (e.g., 1,2)")
    selection = input("Select mappings to send to Manager Review Queue: ").strip().lower()

    # Determine which indexes the analyst selected
    approved_indexes = set()
    if selection == 'all':
        approved_indexes = set(range(1, len(suggestions) + 1))
    elif selection in ['none', 'no', 'exit', '']:
        approved_indexes = set()  # Keep empty
    else:
        try:
            approved_indexes = {int(x.strip()) for x in selection.split(",") if x.strip().isdigit()}
        except ValueError:
            print("Invalid input detected. Treating as 'none' (all mappings dropped).")

    # Loop through suggestions: stage selected items as PENDING, discard unselected items as REJECTED
    for idx, mapping in enumerate(suggestions, 1):
        is_approved_by_analyst = idx in approved_indexes
        
        if is_approved_by_analyst:
            status_string = 'PENDING'  # Sent to Option 2 Manager Queue
            print(f"→ [{idx}] Sent {mapping.get('framework_name')} mapping to Manager Review Queue.")
        else:
            status_string = 'REJECTED' # Filtered out completely
            print(f"✗ [{idx}] Discarded {mapping.get('framework_name')} mapping.")
        
        # Log the decision inside the staging history table
        cursor.execute("""
            INSERT INTO ai_mapping_suggestions (
                internal_control_id, framework_name, suggested_section_id, confidence_score, ai_rationale, status
            ) VALUES (?, ?, ?, ?, ?, ?);
        """, (
            internal_control_db_id,
            mapping.get("framework_name"),
            mapping.get("suggested_section_id"),
            mapping.get("confidence_score"),
            mapping.get("ai_rationale"),
            status_string
        ))

    conn.commit()
    conn.close()
    print("\nInitial ingestion complete. Open Option 3 from the main menu to act as Manager.")


def run_crosswalk_engine_ui(db_path="grc_manager.db"):
    """Terminal UI wrapper for the crosswalk engine, accessible from the main menu."""
    # 1. Ensure tables are established using the dynamic db_path passed from the menu
    print(f"Setting up crosswalk tables in {db_path}...")
    init_crosswalk_tables(db_path=db_path) # Incase DB doesn't exist yet, this will create it and the necessary tables
    
    print("\n=========================================")
    print("   AI GRC Framework Crosswalk Utility   ")
    print("=========================================\n")
    
    while True:
        print("-" * 40)
        user_control_id = input("Enter Control ID (e.g., C-001) or type 'exit' to quit: ").strip()
        
        if user_control_id.lower() == 'exit':
            print("Exiting utility. Returning to AI menu...")
            break
            
        if not user_control_id:
            print("Control ID cannot be empty. Please try again.")
            continue
            
        user_title = input("Enter Control Title: ").strip()
        user_desc = input("Enter Control Description: ").strip()
        
        if not user_title or not user_desc:
            print("Title and Description are both required to generate mappings.")
            continue

        # Operational assembly line
        print("\nAdding control to database...")
        new_id = add_internal_control(
            control_id=user_control_id,
            title=user_title,
            description=user_desc,
            db_path=db_path  # Key Change: Explicitly tell it WHICH database file to target
        )
        
        if new_id:
            print(f"Triggering OpenAI crosswalk generation for Database ID: {new_id}...")
            process_control_crosswalk(new_id, db_path=db_path)  # Key Change: Pass target database to the crosswalk logic
        else:
            print(f"Failed to process. Control ID '{user_control_id}' might already exist.")
        
        print("\n")


def review_suggestions_queue_ui(db_path="grc_manager.db"):
    """Terminal UI to view and process all suggestions currently marked as PENDING."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all suggestions that haven't been approved or rejected yet
    cursor.execute("""
        SELECT s.id, ic.control_id, ic.title, s.framework_name, s.suggested_section_id, s.confidence_score, s.ai_rationale, s.internal_control_id
        FROM ai_mapping_suggestions s
        JOIN internal_controls ic ON s.internal_control_id = ic.id
        WHERE s.status = 'PENDING';
    """)
    pending = cursor.fetchall()

    if not pending:
        print("\n[✓] The Pending Suggestions Queue is completely empty! No items to review.")
        conn.close()
        return

    print(f"\n=========================================")
    print(f"   PENDING AI SUGGESTIONS QUEUE ({len(pending)})   ")
    print("=========================================")

    for row in pending:
        s_id, c_id, c_title, fw_name, sec_id, conf, rationale, ic_db_id = row
        print(f"\n[Suggestion ID: {s_id}] For Control: {c_id} - {c_title}")
        print(f"  → Proposed Framework: {fw_name} ({sec_id})")
        print(f"  → AI Confidence:      {conf}")
        print(f"  → Rationale:          {rationale}")
        print("-" * 40)
        
        choice = input(f"Action for Suggestion {s_id}? (Type 'a' to Approve, 'r' to Reject, 's' to Skip): ").strip().lower()
        
        if choice == 'a':
            # Update status to APPROVED
            cursor.execute("UPDATE ai_mapping_suggestions SET status = 'APPROVED' WHERE id = ?;", (s_id,))
            # Promote to the official active mappings table
            cursor.execute("""
                INSERT INTO framework_mappings (internal_control_id, framework_name, framework_section_id, mapping_rationale)
                VALUES (?, ?, ?, ?);
            """, (ic_db_id, fw_name, sec_id, rationale))
            print(f"✓ Suggestion {s_id} promoted to official mappings.")
        elif choice == 'r':
            cursor.execute("UPDATE ai_mapping_suggestions SET status = 'REJECTED' WHERE id = ?;", (s_id,))
            print(f"✗ Suggestion {s_id} marked as Rejected.")
        else:
            print("→ Skipped for now.")
            
    conn.commit()
    conn.close()
    print("\nQueue review complete.")


# This block handles running this file solo (direct script execution)
if __name__ == "__main__":
    # If executed solo from inside the /app directory, step back to the main DB
    MAIN_DB = "../grc_manager.db"
    run_crosswalk_engine_ui(db_path=MAIN_DB)