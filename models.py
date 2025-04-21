from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, sessionmaker
from database import Base, engine
from datetime import datetime

# --- USERS TABLE ---
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # 'student', 'instructor', 'admin'

    enrollments = relationship("Enrollment", back_populates="user")
    submissions = relationship("Submission", back_populates="user")

# --- COURSES TABLE ---
class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    instructor_id = Column(Integer, ForeignKey('users.id'))

    instructor = relationship("User", foreign_keys=[instructor_id])
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

# --- ENROLLMENTS TABLE ---
class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# --- ASSIGNMENTS TABLE ---
class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)

    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")

# --- SUBMISSIONS TABLE ---
class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    submitted_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")

# --- DISCUSSION POSTS TABLE ---
class DiscussionPost(Base):
    __tablename__ = 'discussion_posts'
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)

# --- CREATE TABLES ---
Base.metadata.create_all(engine)
