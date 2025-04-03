from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models
import schemas
import crud

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canvas Example API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Courses
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_courses(db, skip, limit)

@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

# Enrollments
@app.post("/enrollments/", response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.create_enrollment(db, enrollment)

@app.get("/enrollments/", response_model=List[schemas.Enrollment])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_enrollments(db, skip, limit)

# Assignments
@app.post("/assignments/", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    return crud.create_assignment(db, assignment)

@app.get("/assignments/", response_model=List[schemas.Assignment])
def read_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_assignments(db, skip, limit)

@app.get("/assignments/{assignment_id}", response_model=schemas.Assignment)
def read_assignment(assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = crud.get_assignment(db, assignment_id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment

# Submissions
@app.post("/submissions/", response_model=schemas.Submission)
def create_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    return crud.create_submission(db, submission)

@app.get("/submissions/", response_model=List[schemas.Submission])
def read_submissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_submissions(db, skip, limit)

@app.get("/submissions/{submission_id}", response_model=schemas.Submission)
def read_submission(submission_id: int, db: Session = Depends(get_db)):
    db_submission = crud.get_submission(db, submission_id)
    if not db_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return db_submission
