"""
Mergington High School Club Management System

A comprehensive FastAPI application for managing extracurricular activities,
user accounts, projects, achievements, and club operations at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
import os
from pathlib import Path

from models import (
    engine, create_tables, get_db, User, Activity, Team, Project,
    Achievement, Attendance, Workshop, TechnicalResource, ResourceCategory, Notice
)
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt

# Create database tables
create_tables()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Mergington High School Club Management System",
              description="Comprehensive API for club activities, user management, and achievements")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    interests: Optional[str] = None
    expertise: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    year: Optional[int] = None
    typing_speed: Optional[int] = None
    system_number: Optional[int] = None

class UserResponse(UserBase):
    id: int
    is_mentor: bool
    is_admin: bool
    profile_pic: Optional[str]
    bio: Optional[str]
    interests: Optional[str]
    expertise: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    twitter: Optional[str]
    year: Optional[int]
    resume: Optional[str]
    typing_speed: Optional[int]
    system_number: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    description: str
    schedule: str
    max_participants: int

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    participant_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Initialize default activities if they don't exist
def initialize_default_activities(db: Session):
    default_activities = [
        {
            "name": "Chess Club",
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12
        },
        {
            "name": "Programming Class",
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20
        },
        {
            "name": "Gym Class",
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30
        },
        {
            "name": "Soccer Team",
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22
        },
        {
            "name": "Basketball Team",
            "description": "Practice and play basketball with the school team",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15
        },
        {
            "name": "Art Club",
            "description": "Explore your creativity through painting and drawing",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15
        },
        {
            "name": "Drama Club",
            "description": "Act, direct, and produce plays and performances",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20
        },
        {
            "name": "Math Club",
            "description": "Solve challenging problems and participate in math competitions",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10
        },
        {
            "name": "Debate Team",
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12
        }
    ]

    for activity_data in default_activities:
        activity = db.query(Activity).filter(Activity.name == activity_data["name"]).first()
        if not activity:
            activity = Activity(**activity_data)
            db.add(activity)

    db.commit()

# Routes
@app.on_event("startup")
def startup_event():
    # Initialize database with default data
    db = next(get_db())
    initialize_default_activities(db)

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# Authentication routes
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Activity routes
@app.get("/activities", response_model=List[ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    activities = db.query(Activity).all()
    result = []
    for activity in activities:
        participant_count = len(activity.participants)
        activity_dict = {
            "id": activity.id,
            "name": activity.name,
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participant_count": participant_count,
            "created_at": activity.created_at
        }
        result.append(activity_dict)
    return result

@app.post("/activities/{activity_id}/signup")
def signup_for_activity(activity_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    # Get activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if already signed up
    if current_user in activity.participants:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")

    # Check capacity
    if len(activity.participants) >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add user to activity
    activity.participants.append(current_user)
    db.commit()
    return {"message": f"Signed up {current_user.email} for {activity.name}"}

@app.delete("/activities/{activity_id}/unregister")
def unregister_from_activity(activity_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    # Get activity
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if signed up
    if current_user not in activity.participants:
        raise HTTPException(status_code=400, detail="Not signed up for this activity")

    # Remove user from activity
    activity.participants.remove(current_user)
    db.commit()
    return {"message": f"Unregistered {current_user.email} from {activity.name}"}

# User profile routes
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/users/me", response_model=UserResponse)
async def update_user_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# Team routes
@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return [{"id": team.id, "name": team.name, "description": team.description, "member_count": len(team.members)} for team in teams]

@app.post("/teams")
def create_team(name: str, description: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team = Team(name=name, description=description, created_by_id=current_user.id)
    db.add(team)
    db.commit()
    db.refresh(team)
    return {"message": f"Team '{name}' created", "team_id": team.id}

# Project routes
@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "url": project.url,
        "member_count": len(project.members),
        "created_by": f"{project.created_by.first_name} {project.created_by.last_name}" if project.created_by else None
    } for project in projects]

@app.post("/projects")
def create_project(title: str, description: str, url: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = Project(title=title, description=description, url=url, created_by_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": f"Project '{title}' created", "project_id": project.id}

# Achievement routes
@app.get("/achievements")
def get_achievements(db: Session = Depends(get_db)):
    achievements = db.query(Achievement).all()
    return [{
        "id": achievement.id,
        "title": achievement.title,
        "description": achievement.description,
        "type": achievement.achievement_type,
        "organization": achievement.organization,
        "user": f"{achievement.user.first_name} {achievement.user.last_name}" if achievement.user else None
    } for achievement in achievements]

@app.post("/achievements")
def create_achievement(title: str, description: str, achievement_type: str, organization: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    achievement = Achievement(
        title=title,
        description=description,
        achievement_type=achievement_type,
        organization=organization,
        user_id=current_user.id
    )
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return {"message": f"Achievement '{title}' created", "achievement_id": achievement.id}

# Workshop routes
@app.get("/workshops")
def get_workshops(db: Session = Depends(get_db)):
    workshops = db.query(Workshop).filter(Workshop.is_published == True).all()
    return [{
        "id": workshop.id,
        "name": workshop.name,
        "overview": workshop.overview,
        "level": workshop.level,
        "seats_available": workshop.number_of_seats,
        "trainer": workshop.trainer_bio
    } for workshop in workshops]

@app.post("/workshops")
def create_workshop(name: str, overview: str, level: str, number_of_seats: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    workshop = Workshop(
        name=name,
        overview=overview,
        level=level,
        number_of_seats=number_of_seats,
        created_by_id=current_user.id
    )
    db.add(workshop)
    db.commit()
    db.refresh(workshop)
    return {"message": f"Workshop '{name}' created", "workshop_id": workshop.id}

# Technical Resources routes
@app.get("/resources")
def get_resources(db: Session = Depends(get_db)):
    resources = db.query(TechnicalResource).all()
    return [{
        "id": resource.id,
        "name": resource.name,
        "description": resource.description,
        "category": resource.category.name if resource.category else None,
        "link": resource.link,
        "created_by": f"{resource.created_by.first_name} {resource.created_by.last_name}" if resource.created_by else None
    } for resource in resources]

@app.post("/resources")
def create_resource(name: str, description: str, category_name: str, link: Optional[str] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get or create category
    category = db.query(ResourceCategory).filter(ResourceCategory.name == category_name).first()
    if not category:
        category = ResourceCategory(name=category_name, description=f"Resources for {category_name}")
        db.add(category)
        db.commit()
        db.refresh(category)

    resource = TechnicalResource(
        name=name,
        description=description,
        category_id=category.id,
        link=link,
        created_by_id=current_user.id
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return {"message": f"Resource '{name}' created", "resource_id": resource.id}

# Notice Board routes
@app.get("/notices")
def get_notices(db: Session = Depends(get_db)):
    notices = db.query(Notice).filter(Notice.is_published == True).all()
    return [{
        "id": notice.id,
        "title": notice.title,
        "content": notice.content,
        "created_by": f"{notice.created_by.first_name} {notice.created_by.last_name}" if notice.created_by else None,
        "created_at": notice.created_at
    } for notice in notices]

@app.post("/notices")
def create_notice(title: str, content: str, current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    notice = Notice(
        title=title,
        content=content,
        created_by_id=current_user.id
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return {"message": f"Notice '{title}' created", "notice_id": notice.id}

# Attendance routes
@app.post("/attendance")
def mark_attendance(present: bool, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    attendance = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        func.date(Attendance.date) == today
    ).first()

    if attendance:
        attendance.present = present
    else:
        attendance = Attendance(user_id=current_user.id, date=datetime.utcnow(), present=present)
        db.add(attendance)

    db.commit()
    return {"message": f"Attendance marked as {'present' if present else 'absent'} for {current_user.username}"}

@app.get("/attendance/stats")
def get_attendance_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attendances = db.query(Attendance).filter(Attendance.user_id == current_user.id).all()
    total_days = len(attendances)
    present_days = len([a for a in attendances if a.present])
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    return {
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": total_days - present_days,
        "attendance_percentage": round(attendance_percentage, 2)
    }
