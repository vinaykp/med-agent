import uuid
import json
from toolbox_core import ToolboxClient

# Helper to get a ToolboxClient instance

def get_toolbox_client():
    return ToolboxClient("http://127.0.0.1:5000")

async def list_patients():
    try:
        toolbox_client = get_toolbox_client()
        search_all_patients = await toolbox_client.load_tool("search_all_patients")
        rows = json.loads(await search_all_patients())
        patients = [row["name"] for row in rows]
        return patients if patients else []
    except Exception as e:
        print(f"Error fetching patients: {e}")
        return []

async def get_patient_by_name(name):
    try:
        toolbox_client = get_toolbox_client()
        search_patients_by_name = await toolbox_client.load_tool("search_patients_by_name")
        rows = json.loads(await search_patients_by_name(name=name))
        return rows[0]["data"] if rows else None
    except Exception:
        print(f"Error fetching patient by name: {name}")
        return None

async def load_chat_from_mcp(name):
    try:
        toolbox_client = get_toolbox_client()
        load_chat = await toolbox_client.load_tool("load_chat")
        rows = json.loads(await load_chat(patient_name=name))
        return [(row[0], row[1]) for row in rows]  # sender, message
    except:
        return []

async def save_chat_to_mcp(name, sender, message):
    try:
        toolbox_client = get_toolbox_client()
        save_chat = await toolbox_client.load_tool("save_chat")
        await save_chat(id=str(uuid.uuid4()), patient_name=name, sender=sender, message=message)
    except Exception:
        pass
