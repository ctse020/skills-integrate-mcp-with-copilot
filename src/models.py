from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mergington.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Association tables
activity_participants = Table('activity_participants', Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

project_members = Table('project_members', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

team_members = Table('team_members', Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_mentor = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    profile_pic = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    expertise = Column(Text, nullable=True)
    github = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    resume = Column(String, nullable=True)
    typing_speed = Column(Integer, nullable=True)
    system_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activities = relationship("Activity", secondary=activity_participants, back_populates="participants")
    projects = relationship("Project", secondary=project_members, back_populates="members")
    teams = relationship("Team", secondary=team_members, back_populates="members")
    achievements = relationship("Achievement", back_populates="user")
    attendances = relationship("Attendance", back_populates="user")

# Activity model (replaces the in-memory activities)
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    schedule = Column(String)
    max_participants = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    participants = relationship("User", secondary=activity_participants, back_populates="activities")

# Team model
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    image = Column(String, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")
    members = relationship("User", secondary=team_members, back_populates="teams")

# Project model
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, nullable=True)
    description = Column(Text)
    image = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")
    members = relationship("User", secondary=project_members, back_populates="projects")
    screenshots = relationship("ProjectScreenshot", back_populates="project")
    languages = relationship("ProjectLanguage", back_populates="project")

class ProjectScreenshot(Base):
    __tablename__ = "project_screenshots"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    image = Column(String)

    # Relationships
    project = relationship("Project", back_populates="screenshots")

class ProjectLanguage(Base):
    __tablename__ = "project_languages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    language = Column(String)

    # Relationships
    project = relationship("Project", back_populates="languages")

# Achievement model
class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    achievement_type = Column(String)  # contribution, article, gsoc, contest, etc.
    organization = Column(String, nullable=True)
    url = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="achievements")

# Attendance model
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    present = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="attendances")

# Workshop/Event model
class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    overview = Column(Text)
    course_details = Column(Text, nullable=True)
    project = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    level = Column(String)
    number_of_seats = Column(Integer)
    poster = Column(String, nullable=True)
    trainer_bio = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)
    lab_requirements = Column(Text, nullable=True)
    travel = Column(Text, nullable=True)
    accommodation = Column(Text, nullable=True)
    expense = Column(Integer, nullable=True)
    is_approved = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")

# Technical Resource model
class TechnicalResource(Base):
    __tablename__ = "technical_resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("resource_categories.id"))
    link = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    category = relationship("ResourceCategory", back_populates="resources")
    created_by = relationship("User")

class ResourceCategory(Base):
    __tablename__ = "resource_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)

    # Relationships
    resources = relationship("TechnicalResource", back_populates="category")

# Notice Board model
class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    is_published = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_by = relationship("User")

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()