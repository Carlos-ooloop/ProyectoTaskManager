from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user_model import User
from models.Task_model import Task
from schemas.Task_schema import TaskCreate, TaskResponse,TaskUpdate
from schemas.user_schema import UserCreate,UserResponse,UserUpdate
from utils.auth import hash_password , admin_required , auth_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model= TaskResponse)
async def add_task(task:TaskCreate,db:Session = Depends(get_db), user:User = Depends(admin_required)):
    
    existing_task = db.query(Task).filter(Task.title == task.title, Task.user_id == user.id)
    if existing_task:
        raise HTTPException(status_code=401, detail="USER ALREADY HAS THIS TASK")
    new_task = Task( title = task.title,
                     description = task.description,
                     priority = task.priority,
                     )
    new_task.owner = user
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

@router.get("/my-tasks", response_model= TaskResponse)
async def get_my_task(current_user:User = Depends(auth_user)):
    return current_user.tasks

@router.get("/all", list[TaskResponse])
async def get_all(limit : int = 10, page : int = 1,current_user:User = Depends(admin_required), db: Session = Depends(get_db)):
    offset = (page - 1)*limit 
    return db.query(Task).offset(offset).limit(limit).all()

@router.get("/", response_model= list[TaskResponse])
async def get_by_filter(limit: int = 10, page : int = 1,priority: str|None = None, status: str | None = None,current_user:User = Depends(auth_user), db:Session = Depends(get_db)):
    offset = ( page - 1 )*limit
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)
    return query.offset(offset).limit(limit).all()       

@router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(limit: int = 10, page : int = 1,current_user:User = Depends(auth_user), db : Session = Depends(get_db)):
    offset = (page -1)*limit
    tasks = db.query(Task).filter(Task.user_id == current_user.id).offset(offset).limit(limit).all()
    
    return tasks

@router.get("/{id}", response_model=TaskResponse, dependencies=[Depends(auth_user)])
async def get_single_task(id:int,current_user: User, db:Session = Depends(get_db)):
    
    task = db.query(Task).filter(Task.id==id).first()
    if not task:
        raise HTTPException(status_code=404,detail="TASK NOT FOUND")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="NOT AUTHORIZED")
    
    return task
@router.get("/stats")
async def get_stats(current_user:User = Depends(auth_user), db:Session=Depends(get_db)):
    total_tasks = db.query(Task).filter(Task.user_id == current_user.id).count()
    completed_tasks = db.query(Task).filter(Task.user_id == current_user.id, Task.status == "completed").count()
    pending_tasks = total_tasks - completed_tasks
    low_priority = db.query(Task).filter( Task.user_id == current_user.id, Task.priority == "low").count()
    medium_priority = db.query(Task).filter( Task.user_id == current_user.id, Task.priority == "medium").count()
    high_priority = db.query(Task).filter( Task.user_id == current_user.id, Task.priority == "high").count()
    completion_rate = 0
    if total_tasks > 0:
        completion_rate = (completed_tasks/total_tasks)*100
    return { "total_tasks": total_tasks,
             "completed_tasks": completed_tasks,
             "completion_rate":completion_rate,
             "pending_tasks": pending_tasks,
             "low_priority": low_priority,
             "medium_priority":medium_priority,
             "high_priority": high_priority
             }    
    
    
    
    
    
    
@router.put("/{id}", response_model=TaskResponse)
async def act_task(id:int,task_update :TaskUpdate,current_user:User = Depends(admin_required), db:Session = Depends(get_db)):
    
    task = db.query(Task).filter(Task.id == id).first() 
    if not task:
        raise HTTPException(status_code=404, detail="TASK NOT FOUND")
    if task.user_id != current_user.id:
        raise HTTPException(status_code= 403,detail="NOT AUTHORIZED")   
    if task_update.title:
     task.title = task_update.title
    if task_update.priority:
     task.priority = task_update.priority
    if task_update.description:
     task.description = task_update.description
    
    db.commit()
    db.refresh(task)
    
    return task

@router.delete("/{id}")
async def delete_task(id:int,current_user:User = Depends(admin_required), db:Session = Depends(get_db)):
    
    task  = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code= 404, detail="TASK NOT FOUND")
    if task.user_id != current_user.id:
        raise HTTPException(status_code= 403,detail="NOT AUTHORIZED")   
    db.delete(task)    
    db.commit()
    return {"TASK ELIMINATED SUCCESSFULLY BY":current_user.username}
    
    
