from pydantic import BaseModel,Field,validator
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    

class TaskCreate(BaseModel):
    title : str = Field(min_length= 3 , max_length=100)
    description :str
    priority :str = Field(min_length=3, le=20)
    
class TaskResponse(TaskCreate):
    id : int 
    status :str
    user_id : int
         
class TaskUpdate (BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    priority :Optional[str] = None   
    status : Optional[str] = None
    
@validator("title")
def no_empty(cls,v):
    if not v.strip():
        raise ValueError("TITLE CANNOT BE EMPTY")
    return v    
    
    
    
        