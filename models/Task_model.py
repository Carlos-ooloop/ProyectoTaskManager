from db.database import Base
from sqlalchemy import String,Integer,Column,ForeignKey,Enum,Boolean,DateTime
from sqlalchemy.orm import relationship
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"





class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(Enum(TaskStatus),default=TaskStatus.pending,nullable= False)
    priority = Column(String(20), default="medium")
    user_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User", back_populates= "tasks")
    is_deleted = Column(Boolean, default = False)
    deleted_at = Column(DateTime, nullable = True)