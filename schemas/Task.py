from pydantic import BaseModel

class TaskCreate(BaseModel):
    title : str
    description :str
    priority :str
    
class TaskResponse(TaskCreate):
    id : int 
    status :str
    user_id : int
         