import json      # Standard data interchange format for API payloads and string mapping
from openai import OpenAI   # Main OpenAI API client vehicle for managing chat completion loops
from app.framework_crosswalk import run_crosswalk_engine_ui, review_suggestions_queue_ui

# ------------------------------------------------------------------------------
# SECTION 1: THE CORE AGENT TOOLS (Standard Python Functions)
# ------------------------------------------------------------------------------

def tool_search_risk_register(keyword):
    """
    PURPOSE: Ingests a search term or concept, queries the database 
             using a case-insensitive SQL LIKE constraint on the correct schema,
             and returns all matching Risk IDs and names.
    """
    from database import connect_db
    
    conn = connect_db()
    cursor = conn.cursor()
    
    search_term = f"%{keyword.lower()}%"
    
    cursor.execute("""
        SELECT risk_id, risk_name, treatment_plan 
        FROM risks 
        WHERE LOWER(risk_name) LIKE ? OR LOWER(treatment_plan) LIKE ?
    """, (search_term, search_term))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return json.dumps({"message": f"Discovery Notice: No risks found in the registry matching keyword '{keyword}'."})
        
    results = []
    for r in rows:
        results.append({
            "risk_id": r[0],
            "name": r[1],
            "description": r[2]
        })
        
    return json.dumps(results)


def tool_get_risk_details(risk_id):
    """
    PURPOSE: Ingests a target Risk ID, queries the database, and converts 
             the matching SQLite row attributes into a structured JSON string.
    """
    from database import connect_db
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM risks WHERE UPPER(risk_id) = ?", (risk_id.upper(),))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"Error: Target Risk ID '{risk_id}' was not found within the database register."
    
    fields = [
        "risk_id", "risk_name", "category", "likelihood", "impact", "risk_score", 
        "risk_level", "owner", "treatment_plan", "status", "date_created", 
        "last_review_date", "target_date"
    ]
    
    return json.dumps(dict(zip(fields, row)))


def tool_get_linked_controls(risk_id):
    """
    PURPOSE: Conducts a relational database JOIN check across your junction mapping 
             table to verify what compliance safeguards are actively applied to a risk.
    """
    from database import connect_db
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # DYNAMIC COLUMN PROTECTION: Check the actual column layout to choose between 'control_name' and 'name'
    cursor.execute("PRAGMA table_info(controls)")
    columns = [info[1] for info in cursor.fetchall()]
    name_col = "control_name" if "control_name" in columns else "name"
    
    query = f"""
        SELECT c.control_id, c.{name_col}, c.control_type, c.framework, c.description
        FROM controls c
        JOIN risk_control_mapping m ON c.control_id = m.control_id
        WHERE UPPER(m.risk_id) = ?
    """
    
    cursor.execute(query, (risk_id.upper(),))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"Audit Advisory: There are currently zero mitigating controls mapped to Risk ID {risk_id}."
    
    controls_list = []
    for r in rows:
        controls_list.append({
            "id": r[0],
            "name": r[1],
            "type": r[2],
            "framework": r[3],
            "description": r[4]
        })
        
    return json.dumps(controls_list)


def tool_create_and_link_control(risk_id, control_id, name, control_type, framework, owner, description):
    """
    PURPOSE: Autonomously engineers a mitigation safeguard, saves it to the library, 
             and hooks it to the broken risk target using the join table layout.
    """
    from database import connect_db
    from audit_trail import log_activity
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # DYNAMIC COLUMN PROTECTION
    cursor.execute("PRAGMA table_info(controls)")
    columns = [info[1] for info in cursor.fetchall()]
    name_col = "control_name" if "control_name" in columns else "name"
    
    try:
        query_a = f"""
            INSERT OR REPLACE INTO controls (control_id, {name_col}, control_type, framework, owner, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query_a, (control_id, name, control_type, framework, owner, description))
        
        cursor.execute("""
            INSERT OR REPLACE INTO risk_control_mapping (risk_id, control_id)
            VALUES (?, ?)
        """, (risk_id.upper(), control_id.upper()))
        
        conn.commit()
        log_activity("Agent Remediated Control Gap", f"Autonomously generated and linked control {control_id} to Risk {risk_id}")
        
        return f"Success: Safeguard {control_id} has been saved and permanently linked to Risk {risk_id}."

    except Exception as e:
        conn.rollback()
        return f"Database Error: Failed to create or link control. Reason: {str(e)}"
    finally:
        conn.close()


# ------------------------------------------------------------------------------
# SECTION 2: THE REASONING & ORCHESTRATION CYCLE
# ------------------------------------------------------------------------------

def run_grc_agent(user_input):
    """
    Coordinates state memory tracking loops with OpenAI's completions API 
    and handles deterministic routing to your local python script endpoints.
    """
    client = OpenAI()
    
    messages = [
        {
            "role": "system", 
            "content": (
                "You are an autonomous GRC Compliance Officer. Your goal is to audit risks, "
                "identify security control gaps, and remediate them using your tools. "
                "CRITICAL DIRECTION: If a user specifies a risk by its general name or concept "
                "(e.g., 'firewall', 'passwords', 'backup') instead of providing an explicit Risk ID, "
                "you MUST run 'tool_search_risk_register' first to discover the correct identifier.\n"
                "Always verify existing controls via 'tool_get_linked_controls' before building new ones."
            )
        },
        {
            "role": "user", 
            "content": user_input
        } 
    ]
    
    agent_tools_framework = [
        {
            "type": "function",
            "function": {
                "name": "tool_search_risk_register",
                "description": "Searches the database registry using key-word matching constraints to discover associated Risk IDs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string", 
                            "description": "The target operational concept or search term extracted from the command string (e.g., 'firewall')."
                        }
                    },
                    "required": ["keyword"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "tool_get_risk_details",
                "description": "Queries the database register to get all attributes of a specific risk by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "risk_id": {
                            "type": "string", 
                            "description": "The unique identifier for the risk (e.g., 'R-001')"
                        }
                    },
                    "required": ["risk_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "tool_get_linked_controls",
                "description": "Traverses the three-table bridge to find all security controls currently mapped to a risk.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "risk_id": {
                            "type": "string", 
                            "description": "The target risk ID to inspect."
                        }
                    },
                    "required": ["risk_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "tool_create_and_link_control",
                "description": "Engineers a new mitigation control, saves it, and maps it to the risk via the junction table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "risk_id": {"type": "string", "description": "The risk ID losing protection."},
                        "control_id": {"type": "string", "description": "A unique new identifier for the shield (e.g., 'C-101')"},
                        "name": {"type": "string", "description": "The descriptive title of the control."},
                        "control_type": {"type": "string", "description": "The category (e.g., 'Technical', 'Administrative')"},
                        "framework": {"type": "string", "description": "The compliance framework (e.g., 'SOC 2')"},
                        "owner": {"type": "string", "description": "The corporate employee managing it."},
                        "description": {"type": "string", "description": "Detailed explanation of what the control enforces."}
                    },
                    "required": ["risk_id", "control_id", "name", "control_type", "framework", "owner", "description"]
                }
            }
        }
    ]

    for loop_count in range(5):
        print(f"\n[LOOP {loop_count + 1}/5] Dispatched state context stream to OpenAI...")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=agent_tools_framework,
            tool_choice="auto"  
        )
        
        ai_message = response.choices[0].message
        messages.append(ai_message)
        
        if ai_message.tool_calls:
            for tool_call in ai_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"[EXECUTION TRIGGERED] AI requested local invocation: {tool_name} with args: {tool_args}")
                
                if tool_name == "tool_search_risk_register":
                    tool_output = tool_search_risk_register(**tool_args)
                elif tool_name == "tool_get_risk_details":
                    tool_output = tool_get_risk_details(**tool_args)
                elif tool_name == "tool_get_linked_controls":
                    tool_output = tool_get_linked_controls(**tool_args)
                elif tool_name == "tool_create_and_link_control":
                    tool_output = tool_create_and_link_control(**tool_args)
                else:
                    tool_output = {"error": f"Requested execution endpoint '{tool_name}' isn't structural."}
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_output) if not isinstance(tool_output, str) else tool_output
                })
        else:
            print("\n[GOAL REACHED] Finalized audit report compiled successfully.")
            return ai_message.content

    return "SYSTEM BREAKDOWN ERROR: Agent execution depth broken. Max reasoning loops exceeded."


def ai_services_menu():
    """
    Centralized sub-menu for background automation, analytics, and execution loops.
    Houses the Autonomous GRC Agent loop, crosswalk processors, and staging queues.
    """
    while True:
        print("\n==================================================")
        print("           AGENTIC & AUTOMATED ENGINES            ")
        print("==================================================")
        print("1. Launch Autonomous GRC Agent Loop")
        print("2. Run Crosswalk Suggestion Engine (NIST ↔ ISO ↔ SOC 2)")
        print("3. Review Pending AI Mapping Suggestions Queue")
        print("B. Back to AI Operations Center")
        print("==================================================")
        
        sub_choice = input("Select an engine service: ").strip().upper()
        
        if sub_choice == "1":
            # Option 1: Main Autonomous GRC Agent workflow loop
            print("\n========== Autonomous GRC Agent ==========")
            print("Give the agent a complex objective (e.g., 'Audit Risk R-001 and remediate gaps')")
            print("(Type 'q' or 'quit' to go back)")
            objective = input("\nEnter Agent Objective: ").strip()
            
            if objective.lower() in ['q', 'quit']:
                print("\nExiting agent session...")
                continue  # Returns cleanly back to the Agentic & Automated Engines menu
                
            if objective:
                # Capture the agent's final report and print it to the console cleanly
                final_report = run_grc_agent(objective)
                print("\n=== FINAL AI COMPLIANCE REPORT ===")
                print(final_report)
                print("===================================\n")
            else:
                print("Objective cannot be blank.")
                
        elif sub_choice == "2":
            # Option 2: Triggers crosswalk processing logic
            run_crosswalk_engine_ui()
            
        elif sub_choice == "3":
            # Option 3: Opens human-in-the-loop validation queue interface
            review_suggestions_queue_ui()
            
        elif sub_choice == "B":
            print("Returning to AI Operations Center.")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, or B.")