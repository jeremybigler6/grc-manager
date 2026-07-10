from fastapi import FastAPI
from pydantic import BaseModel
from grc_agent import run_grc_agent

app = FastAPI()

class ObjectiveRequest(BaseModel):
    objective: str

@app.post("/agent/run")
def trigger_agent(data: ObjectiveRequest):
    report = run_grc_agent(data.objective)
    return {"status": "success", "compliance_report": report}