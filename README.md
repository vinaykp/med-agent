
# Med-Agent

A Python project for medical agent automation and tools integration.

## Features
- Modular architecture for medical agent tasks
- Database integration (SQLite)
- Extendable tools for EHR, stock, and more

## Project Structure
```
src/
  app.py                # Main application entry point
  app_cards.py          # Cards-related logic
  app_voice.py          # Voice-related logic
  db/
    db.sql              # Database schema
    medical_agent.db    # SQLite database
  ehr_ai/
    agent.py            # EHR AI agent logic
    __init__.py
  tools/
    db_tools.py         # Database tools
    stock_tools.py      # Stock tools
test/
  ...                   # Test agents and modules
```

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/vinaykp/med-agent.git
   cd med-agent
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run MCP TOOLBOX
To run MCP_TOOLBOX for sqllite
./toolbox --tools-file "/Users/vinaykp/git/med-agent/tools.yaml"

Run the main streamlit application:
```bash
python src/app.py
```

## Testing
Add and run tests in the `src/test/` directory.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

