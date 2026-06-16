# TaskManager Project
## Description:

Task Manager API is a RESTful API built with FastAPI, Python, MySQL and JWT Authentication.
The application allows users to register, authenticate, and manage tasks. Administrators can manage user roles and permissions, while tasks can be organized by status and priority.

The project follows a modular architecture using FastAPI, SQLAlchemy and Pydantic.

 ### Tech Stack:
 -Python 3.14.3
 -FastAPI
 -SQLAlchemy
 -MySQL
 -JWT Authentication
 -Pydantic
 
### Features:
- User registration and authentication
- JWT Access Token and Refresh Token
- User and Admin roles
- User CRUD operations
- Task CRUD operations
- Task status management
- Task priority management
- Soft Delete
- Filtering
- Pagination
- Dashboard statistics
- Logging and activity tracking
  
### Installation:
git clone ...
cd task-manager

python -m venv venv
pip install -r requirements.txt

### Environment variables:
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
TOKEN_DURATION=


### Run the project:
python -m uvicorn main:app --reload

### Project Structure:
ProyectoTaskManager/
├── routers/
├── db/
├── schemas/
├── app/core/
├── services/
├──models/
└── utils/


  
