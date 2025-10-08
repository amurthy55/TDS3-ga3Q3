from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import logging
import json

# Setup logging
logging.basicConfig(filename="agent_runs.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

app = FastAPI()

# Enable CORS for all domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["*"],
)

EMAIL = "25ds2000003@ds.study.iitm.ac.in"
AGENT_NAME = "copilot-cli"  # or whichever CLI agent you choose

def run_agent(task: str) -> str:
    """
    Simulate running a CLI coding agent.
    Replace the command below with your agent CLI, e.g.,
    ['copilot', 'run', '--task', task]
    """
    try:
        # Example: Python one-liner for triangular number if task mentions it
        if "triangular number" in task.lower():
            # Extract the number (naive)
            import re
            n_match = re.search(r'(\d+)', task)
            n = int(n_match.group(1)) if n_match else 1
            output = str(sum(range(1, n+1)))
            return output
        
        # Otherwise, run a generic CLI command
        # result = subprocess.run(["copilot-cli", task], capture_output=True, text=True, timeout=30)
        # return result.stdout.strip()
        return "Simulated output for task: " + task
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/task")
async def handle_task(q: str = Query(..., description="Task description")):
    # output = run_agent(q)

    output = subprocess.run(["copilot-cli", "--task", q], capture_output=True, text=True, timeout=30)
    # return result.stdout.strip()
    
    # Log the run
    logging.info(json.dumps({"task": q, "agent": AGENT_NAME, "output": output}))

    return {
        "task": q,
        "agent": AGENT_NAME,
        # "output": output,
        "output":output.stdout.strip(),
        "email": EMAIL
    }
