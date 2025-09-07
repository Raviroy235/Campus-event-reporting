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
### Setup & Run

To run this project, first create a Python virtual environment and activate it. Then install the required packages from requirements.txt. After that, start the FastAPI app using uvicorn app.main:app --reload. Once it’s running, open your browser and go to http://127.0.0.1:8000/docs to try out the APIs. You can also test them using Postman or curl if you prefer.

### Testing

You can test the APIs using the Swagger UI at /docs in your browser. If you like, you can also use Postman or curl to send requests and see how it works.

### Limitations

Right now, there’s no login or authentication system. The reports are simple text and don’t have any graphs. Also, SQLite is used, so it’s not meant for large-scale use.

### Future Improvements

In the future, I’d like to add login/authentication, maybe make a frontend or mobile app, improve reports with dashboards or graphs, and switch to a bigger database like PostgreSQL for scalability.
