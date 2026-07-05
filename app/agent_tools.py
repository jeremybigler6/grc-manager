# ==============================================================================
# VISUAL ARCHITECTURE REFERENCE: THE AUTONOMOUS AGENT EXECUTION FLOW
# ==============================================================================
# This text diagram tracks how data loops through Section 3 (run_grc_agent).
# Use this to trace the logic when you break down the code.
#
#       +-------------------------------------------------------+
#       | STEP 1: USER INPUT                                    |
#       | "Audit Risk R-001 and remediate gaps"                 |
#       +----------------------------┬--------------------------+
#                                    |
#                                    ▼
#       +-------------------------------------------------------+
#       | STEP 2: REASONING CYCLE STARTS (Max 5 Loops)          |
#       | Ingests entire history array + AGENT_TOOLS framework  |           This is where the loop returns
#       +----------------------------┬--------------------------+
#                                    |
#                                    ▼
#       +-------------------------------------------------------+
#       | STEP 3: OPENAI BRAIN EVALUATION (gpt-4o-mini)          |
#       | Model evaluates the data and makes a decision.         |
#       +----------------------------┬--------------------------+
#                                    |
#                    Does it need to call a tool?
#                    /                          \
#                  YES                           NO (Task Complete)
#                  /                              \
#                 ▼                                ▼
# +---------------------------------+   +----------------------------------+
# | STEP 4: INTERFACE ROUTING       |   | TERMINATION POINT                |
# | AI stops text generation and    |   | Agent outputs final conversational|
# | outputs a structured tool-call  |   | report to the screen.            |        Placed here for the final loop
# | payload request.                |   | Breaks the loop safely.          |
# +----------------┬----------------+   +----------------------------------+
#                  |
#                  ▼
# +---------------------------------+
# | STEP 5: SYSTEM TOOL EXECUTION   |
# | Python runs the chosen tool:    |
# | - tool_get_risk_details()       |
# | - tool_get_linked_controls()    |
# | - tool_create_and_link_control()|
# +----------------┬----------------+
#                  |
#                  ▼
# +---------------------------------+
# | STEP 6: SHORT-TERM MEMORY UPDATE|
# | Database findings are converted  |
# | to JSON and appended back into  |
# | the 'messages' tracking array.  |
# +----------------┬----------------+
#                  |
#                  +---> [Loops back to Step 2 for next inspection check]
#
# ==============================================================================
# GRC PORTFOLIO VALUE:
# Showcasing this specific structural loop in interviews proves you don't just 
# write "wrappers" that look for text. It proves you understand State Management, 
# Loop Boundaries, and deterministic tool constraints in automated corporate governance.
# ==============================================================================


# ==============================================================================
# MODULE: GRC Autonomous Agent Engine
# PURPOSE: Bridges real-time SQLite compliance data with OpenAI's model.
# LICENSE: Open-Source Portfolio Asset (Jeremy Bigler)
# ==============================================================================

import json                 # Standard data interchange format for API payloads and string mapping
from openai import OpenAI   # Main OpenAI API client vehicle for managing chat completion loops

# ------------------------------------------------------------------------------
# SECTION 1: THE CORE AGENT TOOLS (Standard Python Functions)
# ------------------------------------------------------------------------------
# GRC RELEVANCE: An AI model cannot query an enterprise database on its own. 
# These functions serve as bounded execution endpoints. They give the LLM 
# controlled read/write capabilities within your corporate registry.

def tool_get_risk_details(risk_id):
    """
    PURPOSE: Ingests a target Risk ID, queries the database, and converts 
             the matching SQLite row attributes into a structured JSON string.
    """
    # LOCAL IMPORT: Bypasses the initial startup import loop traffic jam completely
    from database import connect_db
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # PARAMETERIZED QUERY: Prevents SQL Injection attacks—an essential security check for auditors. The audit guardrails are in place.
    cursor.execute("SELECT * FROM risks WHERE UPPER(risk_id) = ?", (risk_id.upper(),))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return f"Error: Target Risk ID '{risk_id}' was not found within the database register."
    
    # Normalizing database index parameters to match your documentation schema
    fields = [
        "risk_id", "risk_name", "category", "likelihood", "impact", "risk_score", 
        "risk_level", "owner", "treatment_plan", "status", "date_created", 
        "last_review_date", "target_date"
    ]
    
    # Converts arrays into a Python key-value dict, then packages it into a unified string payload
    return json.dumps(dict(zip(fields, row)))


def tool_get_linked_controls(risk_id):
    """
    PURPOSE: Conducts a relational database JOIN check across your junction mapping 
             table to verify what compliance safeguards are actively applied to a risk.
    """
    # LOCAL IMPORT: Bypasses initial execution memory lockups
    from database import connect_db
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # GRC RELEVANCE: This mimics an automated control-testing verification query.
    cursor.execute("""
        SELECT c.control_id, c.control_name, c.control_type, c.framework, c.description
        FROM controls c
        JOIN risk_control_mapping m ON c.control_id = m.control_id
        WHERE UPPER(m.risk_id) = ?
    """, (risk_id.upper(),))
    
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
    # LOCAL IMPORTS: Isolates operational write logic from platform initialization sequences
    from database import connect_db
    from audit_trail import log_activity
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # DEFENSIVE EXCEPTION HANDLING: Prevents systemic application crashes if a data write error occurs
    try:
        # Step A: Save the fresh safeguard criteria directly into your master control directory
        cursor.execute("""
            INSERT OR REPLACE INTO controls (control_id, control_name, control_type, framework, owner, status, description)
            VALUES (?, ?, ?, ?, ?, 'Active', ?)
        """, (control_id, name, control_type, framework, owner, description))
        
        # Step B: Link the new safeguard directly to the target vulnerability via your junction index table
        cursor.execute("""
            INSERT OR REPLACE INTO risk_control_mapping (risk_id, control_id)
            VALUES (?, ?)
        """, (risk_id.upper(), control_id.upper()))
        
        conn.commit()
        
        # GRC RELEVANCE: Compliance automation mandates automated telemetry audit tracking logs.
        log_activity("Agent Remediated Control Gap", f"Autonomously generated and linked control {control_id} to Risk {risk_id}")
        
        return f"Success: Safeguard {control_id} has been saved and permanently linked to Risk {risk_id}."

    except Exception as e:
        # Rollback prevents database corruption if step A worked but step B failed
        conn.rollback()
        return f"Database Error: Failed to create or link control. Reason: {str(e)}"
    finally:
        conn.close()