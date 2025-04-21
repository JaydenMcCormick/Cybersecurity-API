from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query, Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models
import schemas
import crud
import shutil
import os
import uuid
from pathlib import Path

# Rate limiting imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canvas Example API")

# CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Upload config
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".doc", ".docx"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
@limiter.limit("3/minute")
async def upload_file(assignment_id: int = Form(...), file: UploadFile = File(...), request: Request = None):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    safe_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "original_filename": file.filename,
        "stored_filename": safe_filename,
        "assignment_id": assignment_id,
        "message": "File uploaded successfully"
    }

@app.get("/safe-script/")
def safe_script(script: str = Query(..., enum=["hello", "utility"])):
    allowed_scripts = {
        "hello": "scripts/hello.py",
        "utility": "scripts/utility.py"
    }

    filepath = allowed_scripts.get(script)
    if not filepath or not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Script not found")

    try:
        with open(filepath, "r") as f:
            content = f.read()
        return {
            "script": script,
            "content": content,
            "message": "File safely read, not executed"
        }
    except Exception as e:
        return {"error": str(e)}

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
