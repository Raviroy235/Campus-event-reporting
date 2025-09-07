from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CollegeCreate(BaseModel):
    name: str
    code: Optional[str] = None

class CollegeOut(BaseModel):
    id: int
    name: str
    code: Optional[str]
    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    name: str
    email: Optional[str] = None
    roll_no: Optional[str] = None
    college_id: int

class StudentOut(BaseModel):
    id: int
    name: str
    email: Optional[str]
    roll_no: Optional[str]
    college_id: int
    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    college_id: int
    capacity: Optional[int] = 0

class EventOut(BaseModel):
    id: int
    title: str
    type: str
    college_id: int
    class Config:
        orm_mode = True

class RegisterIn(BaseModel):
    student_id: int

class AttendanceIn(BaseModel):
    student_id: int
    present: bool

class FeedbackIn(BaseModel):
    student_id: int
    rating: int
    comments: Optional[str] = None
