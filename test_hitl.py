# test_hitl.py
import os
import sys
import asyncio
from dotenv import load_dotenv

# 1. Load the environment variables from the Backend directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "Backend"))
load_dotenv(dotenv_path=os.path.join(backend_dir, ".env"))

# 2. Dynamically add the Backend folder to system path
sys.path.insert(0, backend_dir)

from Backend.app.graph.workflow import app as app_graph

async def run_diagnostic():
    # We will pass a highly descriptive, undeniably critical prompt to force the classifier
    initial_state = {
        "account_id": "DIAG_ACC_01",
        "raw_issue_input": "CRITICAL EMERGENCY: Database cluster is completely down. Infrastructure offline throwing 504 gateway timeouts.",
        "extracted_parameters": {},
        "routing_decision": ""
    }
    
    config = {"configurable": {"thread_id": "diagnostic-thread-101"}}
    
    print("Step 1: Invoking graph...")
    final_output = app_graph.invoke(initial_state, config)
    
    print("\nStep 2: Inspecting state values...")
    state_snapshot = app_graph.get_state(config)
    
    # Let's inspect what parameters actually came out of your live agents
    extracted = state_snapshot.values.get("extracted_parameters", {})
    decision = state_snapshot.values.get("routing_decision", "")
    
    print(f"-> Classifier Extracted Parameters: {extracted}")
    print(f"-> Final Routing Decision: {decision}")
    print(f"-> Pending Node: {state_snapshot.next}")
    
    if "human_approval_gate" in state_snapshot.next:
        print("\n✅ SUCCESS: HITL Checkpointer successfully paused the execution!")
    else:
        print("\n❌ FAILED: State did not pause.")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())