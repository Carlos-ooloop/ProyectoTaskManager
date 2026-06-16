from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    username : str
    email : str
    password: str
    
class UserResponse(BaseModel):
    id : int
    username :str
    email : str
    role : str    

class UserUpdate(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
        