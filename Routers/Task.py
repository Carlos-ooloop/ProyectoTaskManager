from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from models.Task import Task
from schemas.Task import TaskCreate, TaskResponse
from schemas.user import UserCreate,UserResponse,UserUpdate
from utils.auth import hash_password , admin_required , auth_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model= TaskResponse)
async def add_task(task:TaskCreate,db:Session = Depends(get_db), user:User = Depends(auth_user)):
    
    existing_task = db.query(Task).filter(Task.title == task.title, Task.user_id == user.id)
    if existing_task:
        raise HTTPException(status_code=401, detail="USER ALREADY HAS THIS TASK")
    new_task = Task( title = task.title,
                     description = task.description,
                     priority = task.priority,
                     user_id = user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
    
    
