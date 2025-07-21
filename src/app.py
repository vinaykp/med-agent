import streamlit as st
import json
from toolbox_core import ToolboxClient # Assuming you install the SDK: pip install toolbox-core
from ehr_ai.agent import run_query  # The agent knows how to call MCP ToolBox
import asyncio
import uuid

# Session state
if "current_patient" not in st.session_state:
    st.session_state.current_patient = None

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------

async def list_patients():
    try:
        toolbox_client = ToolboxClient("http://127.0.0.1:5000")
        search_all_patients = await toolbox_client.load_tool("search_all_patients")
        rows = json.loads(await search_all_patients())
        patients = [row["name"] for row in rows]
        #print(patients)
        return patients if patients else []
    except Exception as e:
        st.error(f"Failed to load patients: {str(e)}")
        return []

async def get_patient_by_name(name):
    #print(f"Fetching patient data for: {name}")
    try:
        toolbox_client = ToolboxClient("http://127.0.0.1:5000")
        search_patients_by_name = await toolbox_client.load_tool("search_patients_by_name")
        rows = json.loads(await search_patients_by_name(name=name))
        return rows[0]["data"] if rows else None
    except Exception:
        st.warning("Failed to load patient data.")
        return None

async def load_chat_from_mcp(name):
    try:
        toolbox_client = ToolboxClient("http://127.0.0.1:5000")
        load_chat = await toolbox_client.load_tool("load_chat")
        rows = json.loads(await load_chat(patient_name=name))
        return [(row[0], row[1]) for row in rows]  # sender, message
    except:
        return []

async def save_chat_to_mcp(name, sender, message):
    try:
        toolbox_client = ToolboxClient("http://127.0.0.1:5000")
        save_chat = await toolbox_client.load_tool("save_chat")
        await save_chat(id=str(uuid.uuid4()), patient_name=name, sender=sender, message=message)
    except Exception as e:
        st.error(f"Failed to save chat: {str(e)}")  

def build_context(patient):
        # Ensure patient is a dict, not a JSON string
    if isinstance(patient, str):
        try:
            patient = json.loads(patient)
        except Exception:
            st.sidebar.error("Patient data is not valid JSON.")
            return
    if not isinstance(patient, dict):
        st.sidebar.error("Patient data is not a valid dictionary.")
        return
    return "\n".join([
        f"Patient: {patient.get('Name')} ({patient.get('Age')}, {patient.get('Gender')})",
        f"ID: {patient.get('Patient ID')}, Blood Group: {patient.get('Blood Group')}",
        f"Diagnosis: {patient.get('Diagnosis')}, Last Visit: {patient.get('Last Visit')}",
        f"Allergies: {patient.get('Allergies')}",
        "Vitals: " + ", ".join(f"{k}: {v}" for k, v in patient.get("Vitals", {}).items()),
        "Medications: " + "; ".join(patient.get("Medications", [])),
        "Lab Results: " + ", ".join(f"{k}: {v}" for k, v in patient.get("Lab Results", {}).items()),
    ])

def show_sidebar(patient):
    # Ensure patient is a dict, not a JSON string
    if isinstance(patient, str):
        try:
            patient = json.loads(patient)
        except Exception:
            st.sidebar.error("Patient data is not valid JSON.")
            return
    if not isinstance(patient, dict):
        st.sidebar.error("Patient data is not a valid dictionary.")
        return
    #print(f"Showing sidebar for patient: {patient}")
    name = patient.get("Name", "Unknown")
    age = patient.get("Age", "-")
    blood_group = patient.get("Blood Group", "-")
    st.sidebar.header(f"{name} ({age}) - {blood_group}")
    with st.sidebar.expander("Personal Details", expanded=True):
        for key in ["Gender", "Patient ID", "Allergies", "Diagnosis", "Last Visit"]:
            st.text(f"{key}: {patient.get(key, '-')}")
    with st.sidebar.expander("Contacts", expanded=False):
        contacts = patient.get("Contacts", {})
        if isinstance(contacts, dict):
            for k, v in contacts.items():
                st.text(f"{k}: {v}")
        else:
            st.text("No contact info available.")
    with st.sidebar.expander("Medication History", expanded=False):
        meds = patient.get("Medications", [])
        if isinstance(meds, list):
            st.text("\n".join(meds) if meds else "No medications listed.")
        else:
            st.text(str(meds))
    with st.sidebar.expander("Family History", expanded=False):
        fam = patient.get("Family History", {})
        if isinstance(fam, dict):
            for k, v in fam.items():
                st.text(f"{k}: {v}")
        else:
            st.text("No family history available.")
    with st.sidebar.expander("Latest Visit Vitals", expanded=True):
        vitals = patient.get("Vitals", {})
        if isinstance(vitals, dict):
            for k, v in vitals.items():
                st.text(f"{k}: {v}")
        else:
            st.text("No vitals available.")
    with st.sidebar.expander("Visit History", expanded=False):
        visits = patient.get("Visit History", [])
        if isinstance(visits, list):
            st.text("\n".join(visits) if visits else "No visit history.")
        else:
            st.text(str(visits))
    with st.sidebar.expander("Lab Results", expanded=False):
        labs = patient.get("Lab Results", {})
        if isinstance(labs, dict):
            for k, v in labs.items():
                st.text(f"{k}: {v}")
        else:
            st.text("No lab results available.")
    with st.sidebar.expander("Billing", expanded=False):
        billing = patient.get("Billing", {})
        if isinstance(billing, dict):
            for k, v in billing.items():
                st.text(f"{k}: {v}")
        else:
            st.text("No billing info available.")

# -------------------------------
st.title("🩺 Medical Agent")

# Sidebar: patient dropdown
with st.sidebar.expander("Select Patient", expanded=True):
    patient_list = asyncio.run(list_patients())
    selected = st.selectbox("Choose a patient", [""] + patient_list)
    selected_name = selected if isinstance(selected, str) else getattr(selected, "name", "")
    if selected_name and selected_name.lower() != st.session_state.current_patient:
        #print(f"Loading patient: {selected_name}")
        patient = asyncio.run(get_patient_by_name(selected_name))
        #print("Patient data::->", patient)
        if patient:
            st.session_state.current_patient = selected_name.lower()
            st.session_state.patient_data = patient
            st.session_state.chat_history = asyncio.run(load_chat_from_mcp(selected_name))
            st.success(f"Loaded patient: {selected_name}")
        else:
            st.warning("Patient not found.")

# Display sidebar cards
if st.session_state.patient_data:
    #print("Session state patient data:", st.session_state.patient_data)
    show_sidebar(st.session_state.patient_data)

# Chat form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")
    async def handle_chat_submit(user_input, patient_name):
        context = build_context(st.session_state.patient_data)
        prompt = f"""Context: {context} User: {user_input}"""
        #print(f"Prompt: {prompt}")
        response = run_query(prompt)
        st.session_state.chat_history.append(("Agent", response))
        st.session_state.chat_history.append(("You", user_input))
        await save_chat_to_mcp(patient_name, "Agent", response)
        await save_chat_to_mcp(patient_name, "You", user_input)

    if submitted and user_input:
        patient_name = st.session_state.current_patient
        asyncio.run(handle_chat_submit(user_input, patient_name))

# Display chat history
for sender, message in reversed(st.session_state.chat_history):
    color = ":blue[**Agent:**]" if sender == "Agent" else ":green[**You:**]"
    st.markdown(f"{color} {message}")
