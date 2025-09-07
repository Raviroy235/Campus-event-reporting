from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import datetime

app = FastAPI(title="Campus Event Reporting")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Simple CRUD endpoints ---

@app.post("/colleges", response_model=schemas.CollegeOut)
def create_college(college: schemas.CollegeCreate, db: Session = Depends(get_db)):
    c = models.College(name=college.name, code=college.code)
    db.add(c)
    try:
        db.commit()
        db.refresh(c)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="College already exists")
    return c

@app.post("/students", response_model=schemas.StudentOut)
def create_student(s: schemas.StudentCreate, db: Session = Depends(get_db)):
    # ensure college exists
    college = db.query(models.College).filter(models.College.id == s.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    st = models.Student(name=s.name, email=s.email, roll_no=s.roll_no, college_id=s.college_id)
    db.add(st)
    db.commit()
    db.refresh(st)
    return st

@app.post("/events", response_model=schemas.EventOut)
def create_event(e: schemas.EventCreate, db: Session = Depends(get_db)):
    college = db.query(models.College).filter(models.College.id == e.college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    ev = models.Event(
        title=e.title, description=e.description, type=e.type,
        start_time=e.start_time, end_time=e.end_time,
        college_id=e.college_id, capacity=e.capacity
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

@app.post("/events/{event_id}/register")
def register_student(event_id: int, payload: schemas.RegisterIn, db: Session = Depends(get_db)):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev or ev.cancelled:
        raise HTTPException(status_code=404, detail="Event not found or cancelled")
    st = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")
    reg = models.Registration(event_id=event_id, student_id=payload.student_id)
    db.add(reg)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Student already registered for this event")
    return {"detail": "Registered"}

@app.post("/events/{event_id}/attendance")
def mark_attendance(event_id: int, payload: schemas.AttendanceIn, db: Session = Depends(get_db)):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev or ev.cancelled:
        raise HTTPException(status_code=404, detail="Event not found or cancelled")
    st = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")

    # auto-register if not registered
    reg = db.query(models.Registration).filter_by(event_id=event_id, student_id=payload.student_id).first()
    if not reg:
        reg = models.Registration(event_id=event_id, student_id=payload.student_id)
        db.add(reg)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

    # mark attendance (create or update)
    att = db.query(models.Attendance).filter_by(event_id=event_id, student_id=payload.student_id).first()
    if not att:
        att = models.Attendance(event_id=event_id, student_id=payload.student_id, present=payload.present, checkin_time=(datetime.datetime.utcnow() if payload.present else None))
        db.add(att)
    else:
        att.present = payload.present
        att.checkin_time = (datetime.datetime.utcnow() if payload.present else None)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not record attendance")
    return {"detail": "Attendance recorded"}

@app.post("/events/{event_id}/feedback")
def submit_feedback(event_id: int, payload: schemas.FeedbackIn, db: Session = Depends(get_db)):
    ev = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not ev or ev.cancelled:
        raise HTTPException(status_code=404, detail="Event not found or cancelled")
    st = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found")

    # require registration (or attendance) before feedback
    reg = db.query(models.Registration).filter_by(event_id=event_id, student_id=payload.student_id).first()
    if not reg:
        raise HTTPException(status_code=400, detail="Student did not register (cannot submit feedback)")

    fb = models.Feedback(event_id=event_id, student_id=payload.student_id, rating=payload.rating, comments=payload.comments)
    db.add(fb)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Feedback already submitted")
    return {"detail": "Feedback submitted"}

# --- Reports ---

@app.get("/reports/event_popularity")
def event_popularity(college_id: int = None, event_type: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Event.id, models.Event.title, func.count(models.Registration.id).label("registrations"))\
          .outerjoin(models.Registration, models.Event.id == models.Registration.event_id)\
          .group_by(models.Event.id)\
          .order_by(func.count(models.Registration.id).desc())

    if college_id:
        q = q.filter(models.Event.college_id == college_id)
    if event_type:
        q = q.filter(models.Event.type == event_type)
    res = [{"event_id": r.id, "title": r.title, "registrations": r.registrations} for r in q.all()]
    return res

@app.get("/reports/student_participation")
def student_participation(student_id: int = None, college_id: int = None, db: Session = Depends(get_db)):
    q = db.query(models.Student.id, models.Student.name, func.count(models.Attendance.id).label("events_attended"))\
          .outerjoin(models.Attendance, (models.Student.id == models.Attendance.student_id) & (models.Attendance.present == True))\
          .group_by(models.Student.id)\
          .order_by(func.count(models.Attendance.id).desc())

    if student_id:
        q = q.filter(models.Student.id == student_id)
    if college_id:
        q = q.filter(models.Student.college_id == college_id)

    res = [{"student_id": r.id, "name": r.name, "events_attended": r.events_attended} for r in q.all()]
    return res

@app.get("/reports/top_active_students")
def top_active_students(college_id: int = None, limit: int = 3, db: Session = Depends(get_db)):
    q = db.query(models.Student.id, models.Student.name, func.count(models.Attendance.id).label("events_attended"))\
          .outerjoin(models.Attendance, (models.Student.id == models.Attendance.student_id) & (models.Attendance.present == True))\
          .group_by(models.Student.id)\
          .order_by(func.count(models.Attendance.id).desc())\
          .limit(limit)
    if college_id:
        q = q.filter(models.Student.college_id == college_id)
    return [{"student_id": r.id, "name": r.name, "events_attended": r.events_attended} for r in q.all()]

@app.get("/reports/event_stats/{event_id}")
def event_stats(event_id: int, db: Session = Depends(get_db)):
    # registrations
    reg_count = db.query(func.count(models.Registration.id)).filter(models.Registration.event_id == event_id).scalar() or 0
    attended_count = db.query(func.count(models.Attendance.id)).filter(models.Attendance.event_id == event_id, models.Attendance.present == True).scalar() or 0
    avg_feedback = db.query(func.avg(models.Feedback.rating)).filter(models.Feedback.event_id == event_id).scalar()
    attendance_pct = (attended_count * 100.0 / reg_count) if reg_count > 0 else 0.0
    return {
        "event_id": event_id,
        "registrations": reg_count,
        "attended": attended_count,
        "attendance_percent": round(attendance_pct, 2),
        "avg_feedback": round(avg_feedback, 2) if avg_feedback is not None else None
    }
