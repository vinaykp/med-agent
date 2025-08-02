import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from google.adk.cli.fast_api import get_fast_api_app

import tools.ehr_tools as ehr_tools
from ehr_ai.agent import root_agent, run_query

# Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR  # Parent directory containing multi_tool_agent

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str


class SaveChatRequest(BaseModel):
    name: str
    sender: str
    message: str

# Create the FastAPI app using ADK's helper
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    allow_origins=["*"],  # In production, restrict this
    web=True,  # Enable the ADK Web UI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agent-info")
async def agent_info():
    """Provide agent information"""

    return {
        "agent_name": root_agent.name,
        "description": root_agent.description,
        "model": root_agent.model,
        "tools": [str(tool) for tool in root_agent.tools],
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    print(f"Received query: {request.query}")
    result = run_query(request.query)
    return QueryResponse(response=result)

@app.get("/patients", response_model=List[str])
async def get_patients():
    return await ehr_tools.list_patients()

@app.get("/patient/{name}")
async def get_patient(name: str):
    print(f"Fetching patient by name: {name}")
    return await ehr_tools.get_patient_by_name(name)

@app.get("/chat/load/{name}")
async def load_chat(name: str):
    return await ehr_tools.load_chat_from_mcp(name)

@app.post("/chat/save")
async def save_chat(request: SaveChatRequest):
    await ehr_tools.save_chat_to_mcp(request.name, request.sender, request.message)
    return {"status": "ok"}

if __name__ == "__main__":
    # Run as web server (default)
    print("Starting Web server mode...")
    uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000, 
            reload=False
    )





