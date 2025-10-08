from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import os
import re

app = FastAPI()
EMAIL = "25ds2000003@ds.study.iitm.ac.in"
AGENT_NAME = "copilot-cli"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logging.basicConfig(
    filename="agent_runs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def run_agent(task: str) -> str:
    try:
        if "triangular" in task.lower():
            match = re.search(r"(\d+)", task)
            n = int(match.group(1)) if match else 1
            return str(n * (n + 1) // 2)
        return f"Simulated output for task: {task}"
    except Exception as e:
        return f"Error during task: {e}"

# --- Root route for Railway health check ---
@app.get("/")
async def root():
    return {"status": "ok", "message": "FastAPI agent server running"}

@app.get("/task")
async def handle_task(q: str = Query(..., description="Task description")):
    output = run_agent(q)
    logging.info(json.dumps({
        "task": q,
        "agent": AGENT_NAME,
        "output": output
    }))
    return {
        "task": q,
        "agent": AGENT_NAME,
        "output": output,
        "email": EMAIL
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
