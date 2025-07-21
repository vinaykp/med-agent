from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
import uuid
import asyncio

from tools.db_tools import db_tools

load_dotenv()

#model=LiteLlm(model="huggingface/featherless-ai/google/medgemma-4b-it"),
#model=LiteLlm(model="ollama_chat/gemma3n:latest"), # doesnt support tools
#LLM_MODEL=LiteLlm(model="ollama_chat/alibayram/medgemma:latest"), # doesnt support tools
#LLM_MODEL=LiteLlm(api_base="http://localhost:11434/v1",model="openai/qwen3:1.7b",api_key="ollama")
#LLM_MODEL="gemini-2.5-flash"
LLM_MODEL = LiteLlm(model="nvidia_nim/meta/llama-3.3-70b-instruct")

from tools.stock_tools import get_stock_price  # Make sure this import points to your actual tool implementation

stock_agent = LlmAgent(
    name="StockAgent",
    description="Agent for stock-related queries.",
    model=LLM_MODEL,
    instruction="""
    You can answer questions about stock prices, trends, and market analysis.
    Use the 'get-stock-price' tool to retrieve stock prices.
    If you cannot find the information, inform the user that you are unable to retrieve it.
    """,
    tools=[get_stock_price]
)

patient_agent = LlmAgent(
    name="PatientAgent",
    description="Patient information agent.",
    model=LiteLlm(model="ollama_chat/alibayram/medgemma:latest"),
    instruction="""
    You can answer questions about patient details, medical history, medications, and more.
    Also, you can answer summary questions about the patient's health.
    You must use db_tools to retrieve information.
    If you need to create a new patient record, use the 'create-patients-by-name' tool.
    If you need to search for existing patients, use the 'search-patients-by-name' tool to retrieve patient details.
    If you need to retrieve all patients, use the 'search-all-patients' tool.
    When using tools, ensure you provide the necessary parameters as specified in the tool definitions.
    If you cannot find the information, inform the user that you are unable to retrieve it.
    """,
    tools=list(db_tools)
)

root_agent = LlmAgent(
    name="RootAgent",
    description="Root agent that can delegate tasks to specialized agents.",
    model=LLM_MODEL,
    instruction="""
    You can delegate tasks to specialized agents.
    If you cannot find the information, inform the user that you are unable to retrieve it.
    Use the 'StockAgent' for stock-related queries and 'PatientAgent' for patient and medical queries.
    Ensure you use the appropriate agent based on the user's query.
    """,
    tools=[AgentTool(agent=stock_agent), AgentTool(agent=patient_agent)]
)
agent = root_agent

# --- Constants ---
APP_NAME = "med-agent"
USER_ID = "test_user"
SESSION_ID = f"session_{uuid.uuid4()}"

# --- Session and Runner Setup ---
session_service = InMemorySessionService()
# Use asyncio.run() to execute the async session creation**
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
))

runner = Runner(agent=agent, session_service=session_service, app_name=APP_NAME)

def run_query(query: str) -> str:
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    # Process events to get the final response
    for event in events:
        if event.is_final_response():
            return event.content.parts[0].text # type: ignore
    return "No response received."