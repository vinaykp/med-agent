from toolbox_core import ToolboxSyncClient

# Initialize the ToolboxSyncClient with the URL of the toolbox server
# and load the toolset for EHR operations.
# SQLite DB define at tools.yaml, database path: "/Users/vinaykp/git/med-agent/db/database.db"
# Run in terminal from toolbox installed: ./toolbox --tools-file "/Users/vinaykp/git/med-agent/tools.yaml"

toolbox_client = ToolboxSyncClient("http://127.0.0.1:5000")
db_tools = toolbox_client.load_toolset("ehr_toolset")