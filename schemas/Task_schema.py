from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title : str
    description :str
    priority :str
    
class TaskResponse(TaskCreate):
    id : int 
    status :str
    user_id : int
         
class TaskUpdate (BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    priority :Optional[str] = None   
    status : Optional[str] = None    