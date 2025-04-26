from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Literal, Annotated
from datetime import datetime

# Reusable types
NameType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
TitleType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
DescriptionType = Annotated[str, StringConstraints(strip_whitespace=True, max_length=1000)]
ContentType = Annotated[str, StringConstraints(strip_whitespace=True, max_length=10000)]

# User schemas
class UserBase(BaseModel):
    name: NameType
    email: EmailStr
    role: Literal["student", "instructor", "admin"]

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Course schemas
class CourseBase(BaseModel):
    title: TitleType
    description: Optional[DescriptionType] = None
    instructor_id: Optional[int] = None

class CourseCreate(CourseBase): pass

class Course(CourseBase):
    id: int
    model_config = {"from_attributes": True}

# Enrollment schemas
class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase): pass

class Enrollment(EnrollmentBase):
    id: int
    model_config = {"from_attributes": True}

# Assignment schemas
class AssignmentBase(BaseModel):
    course_id: int
    title: TitleType
    description: Optional[DescriptionType] = None
    due_date: Optional[datetime] = None

class AssignmentCreate(AssignmentBase): pass

class Assignment(AssignmentBase):
    id: int
    model_config = {"from_attributes": True}

# Submission schemas
class SubmissionBase(BaseModel):
    assignment_id: int
    user_id: int
    content: Optional[ContentType] = None

class SubmissionCreate(SubmissionBase): pass

class Submission(SubmissionBase):
    id: int
    submitted_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

# Discussion post schemas
class DiscussionPostBase(BaseModel):
    author: str
    content: str

class DiscussionPostCreate(DiscussionPostBase): pass

class DiscussionPost(DiscussionPostBase):
    id: int
    model_config = {"from_attributes": True}
