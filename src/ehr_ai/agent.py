import uuid
import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

#LLM_MODEL="gemini-2.5-flash"
LLM_MODEL = LiteLlm(model="cerebras/qwen-3-32b") # qwen-3-32b or llama-3.3-70b , qwen-3-235b-a22b-thinking-2507

medical_agent = LlmAgent(
    name="medical_agent",
    description="Medical information agent.",
    model=LiteLlm(model="ollama_chat/alibayram/medgemma:latest"),
    instruction="""
    You are expert in medical information and can provide concise answers to medical queries.
    You can answer medical-related queries, including symptoms, treatments, and medical conditions.
    Use patient information in context to provide accurate medical advice.
    Don't add disclaimer to your response.
    """
)

root_agent = LlmAgent(
    name="RootAgent",
    description="Root agent that can delegate tasks to specialized agents.",
    model=LLM_MODEL, 
    instruction="""
    You can delegate tasks to specialized agents.
    Use the 'medical_agent' for medical-related queries.
    For general queries use web_agent search.
    All responses should be concise and to the point.
    Ensure you use the appropriate agent based on the user's query.
    """,
    tools=[AgentTool(agent=medical_agent)]
    #sub_agents=[medical_agent]
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
    print(f"Running query in agent: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    # Process events to get the final response
    print(f"Processing events to get final response... {events}" )
    for event in events:
        if event.is_final_response():
            return event.content.parts[0].text # type: ignore
    return "No response received."
