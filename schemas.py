from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # 'student', 'instructor', 'admin'

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Course Schemas
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructor_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True

# Enrollment Schemas
class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True

# Assignment Schemas
class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int

    class Config:
        orm_mode = True

# Submission Schemas
class SubmissionBase(BaseModel):
    assignment_id: int
    user_id: int
    content: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    submitted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
