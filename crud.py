from sqlalchemy.orm import Session
from models import User, Course, Enrollment, Assignment, Submission
import schemas

# Users
def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Courses
def create_course(db: Session, course: schemas.CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

# Enrollments
def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

def get_enrollments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Enrollment).offset(skip).limit(limit).all()

# Assignments
def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignment(db: Session, assignment_id: int):
    return db.query(Assignment).filter(Assignment.id == assignment_id).first()

def get_assignments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Assignment).offset(skip).limit(limit).all()


# Submissions
def create_submission(db: Session, submission: schemas.SubmissionCreate):
    db_submission = Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def get_submission(db: Session, submission_id: int):
    return db.query(Submission).filter(Submission.id == submission_id).first()

def get_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Submission).offset(skip).limit(limit).all()
