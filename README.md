# Campus Event Reporting System

## About this repo
This is my small project for a campus event reporting system. I tried to build a simple backend using **FastAPI** with an **SQLite** database.  
It is not a full-fledged web or mobile app, but just the backend with APIs and some basic reporting features to test out the idea.

---

## What’s included
- FastAPI app inside the `app/` folder  
- SQLite database file (`events.db`)  
- Endpoints to add **colleges, students, and events**  
- APIs to:
  - Register students for events  
  - Mark student attendance  
  - Submit feedback  
- Reporting APIs for:
  - Event popularity  
  - Student participation  
  - Top active students  
  - Event statistics  

---

## Setup & Run

Follow these steps to set up the project locally:

### 1. Clone the repository
```bash
git clone <repo_url>
cd <repo_name>

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Run the FastAPI app
bash
Copy code
uvicorn app.main:app --reload
5. Open your browser
Go to:

arduino
Copy code
http://127.0.0.1:8000/docs
to test the APIs with Swagger UI.

Testing
You can test the APIs in two ways:

Swagger UI (auto-generated at /docs)

Postman / curl for sending custom requests

Example:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/students/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "college_id": 1}'
Limitations
No authentication or login system yet

Reports are basic text output (no visualizations)

Not optimized for scaling (SQLite is used just for simplicity)

Future Improvements
Add authentication (JWT, role-based access)

Build a simple frontend or mobile client

Improve reporting with dashboards/graphs

Migrate from SQLite to PostgreSQL/MySQL for scalability
