from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=True)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    roll_no = Column(String, nullable=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    college = relationship("College")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=False)   # e.g., Workshop, Fest, Seminar
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    capacity = Column(Integer, nullable=True)
    cancelled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    college = relationship("College")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("event_id", "student_id", name="uix_event_student"),)
    event = relationship("Event")
    student = relationship("Student")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    present = Column(Boolean, default=False)
    checkin_time = Column(DateTime, nullable=True)
    __table_args__ = (UniqueConstraint("event_id", "student_id", name="uix_attendance_event_student"),)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("event_id", "student_id", name="uix_feedback_event_student"),)
