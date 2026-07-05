# Orchestrator: GRC Agent

import json
from openai import OpenAI

# Pull in the 3 secure database tools we broke down earlier
from agent_tools import (
    tool_get_risk_details, 
    tool_get_linked_controls, 
    tool_create_and_link_control
)

def run_grc_agent(user_input):
    """
    The Central Orchestrator: Manages the 5-loop execution cycle, 
    talk to the OpenAI API, and runs local tools based on AI decisions.
    """
    # Initialize the secure connection to OpenAI's server infrastructure
    client = OpenAI()
    
    # Initialize the short-term memory 'notebook' tracking array
    messages = [
        {
            "role": "system", 
            "content": (
                "You are an autonomous GRC Compliance Officer. Your goal is to audit risks, "
                "identify security control gaps, and remediate them using your tools. "
                "Always verify existing controls before creating new ones."
            )
        },
        {"role": "user", "content": user_input}  # Step 1: Ingest the user's prompt
    ]
    
    # Define the tool blueprint dictionary so OpenAI knows what tools exist
    agent_tools_framework = [
        {
            "type": "function",
            "function": {
                "name": "tool_get_risk_details",
                "description": "Queries the database register to get all attributes of a specific risk by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "risk_id": {"type": "string", "description": "The unique identifier for the risk (e.g., 'R-001')"}
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
                        "risk_id": {"type": "string", "description": "The target risk ID to inspect."}
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

    # STEP 2: The Reasoning Cycle (Max 5 Loops Safety Guardrail)
    for loop_count in range(5):
        print(f"\n[LOOP {loop_count + 1}/5] Reaching out to OpenAI brain...")
        
        # STEP 3: THE HANDSHAKE LINE - Sending the notebook data over the internet
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=agent_tools_framework,
            tool_choice="auto"  # Let the AI choose whether to call a tool or finish
        )
        
        # Intercept the response envelope
        ai_message = response.choices[0].message
        
        # Append the AI's thoughts back into our local notebook array
        messages.append(ai_message)
        
        # EVALUATION POINT: Does it need to call a tool?
        if not ai_message.tool_calls:
            # NO path taken (Task Complete): Exit the loop and return the final report
            print("[EXIT] Task complete. Terminating loop.")
            return ai_message.content
            
        # YES path taken: Route to STEP 4 & 5 (System Execution)
        print(f"-> AI requested {len(ai_message.tool_calls)} tool execution(s).")
        
        for tool_call in ai_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"   Executing local Python tool: {function_name}() with arguments: {function_args}")
                
            # === THE ROUTER: Physically running your local code based on OpenAI's instruction ===
            if function_name == "tool_get_risk_details":
                tool_output = tool_get_risk_details(risk_id=function_args.get("risk_id"))
            elif function_name == "tool_get_linked_controls":
                tool_output = tool_get_linked_controls(risk_id=function_args.get("risk_id"))
            elif function_name == "tool_create_and_link_control":
                tool_output = tool_create_and_link_control(
                    risk_id=function_args.get("risk_id"),
                    control_id=function_args.get("control_id"),
                    name=function_args.get("name"),
                    control_type=function_args.get("control_type"),
                    framework=function_args.get("framework"),
                    owner=function_args.get("owner"),
                    description=function_args.get("description")
                )
            else:
                tool_output = f"Error: Tool '{function_name}' is not integrated into this system."
                
            # === THE MEMORY BANK: Appending the raw tool database results back to the notebook ===
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_output
            })
            print(f"   Stored tool results inside short-term memory array.")

    # Safety trap if it exhausts all 5 loops without cleanly exiting
    return "Error: Agent timed out. Maximum logic execution guardrail threshold exceeded."


# === THE ENTRY POINT: Allows execution directly from the command line ===
if __name__ == "__main__":
    print("--- GRC Risk Management Agent Active ---")
    prompt = input("Enter your compliance instruction (e.g., 'Check risk details for R-001'): ")
    
    if prompt.strip():
        final_report = run_grc_agent(prompt)
        print("\n=== FINAL AGENT REPORT ===")
        print(final_report)
    else:
        print("No instruction provided. Exiting.")