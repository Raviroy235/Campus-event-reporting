from app.database import SessionLocal, engine
import app.models as models
import datetime

def seed():
    db = SessionLocal()
    try:
        # colleges
        c1 = models.College(name="ABC College", code="ABC")
        c2 = models.College(name="XYZ Institute", code="XYZ")
        db.add_all([c1, c2])
        db.commit()

        # students
        s1 = models.Student(name="John Doe", email="john@example.com", roll_no="CS101", college_id=c1.id)
        s2 = models.Student(name="Jane Smith", email="jane@example.com", roll_no="CS102", college_id=c1.id)
        s3 = models.Student(name="Ravi Kumar", email="ravi@example.com", roll_no="CS103", college_id=c2.id)
        db.add_all([s1, s2, s3])
        db.commit()

        # events
        e1 = models.Event(title="Intro to AI", description="Workshop on AI", type="Workshop",
                          start_time=datetime.datetime(2025,9,10,9,0), end_time=datetime.datetime(2025,9,10,12,0),
                          college_id=c1.id)
        e2 = models.Event(title="Tech Fest", description="Annual fest", type="Fest",
                          start_time=datetime.datetime(2025,9,15,10,0), end_time=datetime.datetime(2025,9,15,18,0),
                          college_id=c1.id)
        db.add_all([e1, e2])
        db.commit()

        # registrations
        r1 = models.Registration(event_id=e1.id, student_id=s1.id)
        r2 = models.Registration(event_id=e1.id, student_id=s2.id)
        r3 = models.Registration(event_id=e2.id, student_id=s2.id)
        db.add_all([r1, r2, r3])
        db.commit()

        # attendance
        a1 = models.Attendance(event_id=e1.id, student_id=s1.id, present=True)
        a2 = models.Attendance(event_id=e1.id, student_id=s2.id, present=False)
        db.add_all([a1, a2])
        db.commit()

        # feedback
        f1 = models.Feedback(event_id=e1.id, student_id=s1.id, rating=5, comments="Great!")
        db.add(f1)
        db.commit()

        print("Seed data inserted.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
