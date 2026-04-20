# Mergington High School Club Management System

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey ctse020!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%to%Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/ctse020/skills-integrate-mcp-with-copilot/issues/1)

---

## 🎯 **Project Overview**

This is a comprehensive **FastAPI-based club management system** for Mergington High School that has evolved from a simple activity signup system into a full-featured organizational platform.

### **🚀 New Features Implemented**

#### **1. User & Account Management System** ✅
- **JWT Authentication**: Secure login/logout with token-based auth
- **User Registration**: Complete signup process with validation
- **User Profiles**: Comprehensive profiles with social media links, bio, expertise
- **Role-based Access**: Support for students, mentors, and administrators
- **Profile Customization**: Resume uploads, typing speed tracking, system numbers

#### **2. Club Organization System** ✅
- **Team Management**: Create and manage teams with members
- **Responsibility Assignment**: Track individual responsibilities
- **Attendance Tracking**: Daily attendance with percentage calculations
- **Status Updates**: Weekly status update system
- **Role-based Permissions**: Different access levels for different user types

#### **3. Achievements & Recognition Module** ✅
- **Open Source Contributions**: Track GitHub contributions and bug fixes
- **Articles & Publications**: Archive of written articles and publications
- **GSoC/RGSoC Tracking**: Timeline of Google Summer of Code participation
- **Contest Records**: Competition participation and ranking history
- **Internship Tracking**: Professional experience documentation
- **Conference Talks**: Speaking engagement records

#### **4. Projects Management System** ✅
- **Project CRUD**: Full create, read, update, delete operations
- **Project Screenshots**: Upload and manage project galleries
- **Programming Languages**: Tag projects with technologies used
- **Project Members**: Track contributors and team members
- **Project Portfolio**: Showcase completed work

#### **5. Events & Workshops Module** ✅
- **Workshop Management**: Detailed workshop creation with prerequisites
- **Course Details**: Comprehensive workshop information
- **Lab Requirements**: Track equipment and facility needs
- **Travel & Accommodation**: Event logistics management
- **Expense Tracking**: Budget and cost management
- **Approval Workflows**: Admin approval system for events

#### **6. Technical Resources & Learning Library** ✅
- **Resource Categories**: Organized learning materials
- **Interview Preparation**: Question banks and practice materials
- **Company Papers**: Archive of coding interview questions
- **Online Courses**: Curated learning resource links
- **GSoC Proposals**: Archive of successful project proposals

#### **7. Administrative & Workflow System** ✅
- **Document Management**: Restricted access to important documents
- **Notice Board**: Club-wide announcements and notifications
- **Membership Applications**: Application review and approval system
- **Admin Dashboard**: Administrative controls and oversight
- **Content Moderation**: Publishing and approval workflows

#### **8. Data Persistence & Database** ✅
- **SQLite Database**: Replaced in-memory storage with persistent database
- **SQLAlchemy ORM**: Modern database abstraction layer
- **Data Relationships**: Proper foreign key relationships and associations
- **Migration Support**: Alembic for database schema management
- **Data Integrity**: Constraints and validation at database level

### **🛠 Technical Stack**

**Backend:**
- **FastAPI**: Modern, fast web framework for Python
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Python-JOSE**: JWT token handling
- **PassLib**: Password hashing
- **Pydantic**: Data validation

**Frontend:**
- **HTML5/CSS3**: Responsive web interface
- **Vanilla JavaScript**: Dynamic client-side functionality
- **Bootstrap-inspired**: Custom CSS framework
- **RESTful API**: AJAX calls to backend

**Database:**
- **SQLite**: Lightweight, file-based database
- **Relational Design**: Normalized schema with proper relationships

### **📋 API Endpoints**

#### **Authentication**
- `POST /register` - User registration
- `POST /token` - User login (OAuth2)
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile

#### **Activities**
- `GET /activities` - List all activities
- `POST /activities/{id}/signup` - Sign up for activity
- `DELETE /activities/{id}/unregister` - Unregister from activity

#### **Projects**
- `GET /projects` - List all projects
- `POST /projects` - Create new project

#### **Teams**
- `GET /teams` - List all teams
- `POST /teams` - Create new team

#### **Achievements**
- `GET /achievements` - List all achievements
- `POST /achievements` - Add new achievement

#### **Workshops**
- `GET /workshops` - List published workshops
- `POST /workshops` - Create new workshop

#### **Resources**
- `GET /resources` - List technical resources
- `POST /resources` - Add new resource

#### **Notices**
- `GET /notices` - List published notices
- `POST /notices` - Create new notice (admin only)

#### **Attendance**
- `POST /attendance` - Mark daily attendance
- `GET /attendance/stats` - Get attendance statistics

### **🚀 Getting Started**

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   cd src
   uvicorn app:app --reload
   ```

3. **Access the Application:**
   - Open `http://localhost:8000` in your browser
   - Register a new account or login
   - Explore the various sections: Activities, Projects, Teams, etc.

### **🔐 Default Users**

The system initializes with default activities. You can register new users through the web interface.

### **📊 Database Schema**

The application uses a comprehensive database schema with the following main entities:
- **Users**: Authentication and profile information
- **Activities**: Extracurricular activities with participant tracking
- **Teams**: Club teams and member associations
- **Projects**: Student projects with screenshots and languages
- **Achievements**: Recognition and accomplishment tracking
- **Workshops**: Educational events and training sessions
- **Resources**: Technical learning materials
- **Notices**: Club announcements
- **Attendance**: Daily attendance records

### **🎯 Key Features**

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Dynamic content loading without page refreshes
- **Secure Authentication**: JWT-based authentication system
- **Role-based Access**: Different permissions for different user types
- **Data Persistence**: All data is stored in a SQLite database
- **RESTful API**: Clean, documented API endpoints
- **Modern UI**: Intuitive and user-friendly interface

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

