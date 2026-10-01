# FitBuddy – AI Fitness Plan Generator

FastAPI + Jinja2 + SQLite + Google Gemini project based on the supplied project specification.

## Folder structure

FitBuddy/
- app/
  - __init__.py
  - main.py
  - routes.py
  - database.py
  - schemas.py
  - gemini_generator.py
  - gemini_flash_generator.py
  - updated_plan.py
- templates/
  - index.html
  - result.html
  - all_users.html
- static/
  - style.css
  - images/fitness-bg.svg
- requirements.txt
- .env.example
- .gitignore
- README.md

## Windows setup

1. Open Command Prompt in the FitBuddy folder.
2. Create environment:
   python -m venv venv
3. Activate:
   venv\\Scripts\\activate
4. Install:
   pip install -r requirements.txt
5. Create `.env` from `.env.example` and add your Gemini API key.
6. Set the key in Command Prompt:
   set GOOGLE_API_KEY=your_gemini_api_key_here
7. Start:
   uvicorn app.main:app --reload
8. Open http://127.0.0.1:8000
9. API docs: http://127.0.0.1:8000/docs

The database file `fitbuddy.db` is created automatically on first run.
