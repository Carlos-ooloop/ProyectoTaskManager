from db.database import Base
from sqlalchemy import String,Integer,Column,ForeignKey

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(String(20),default="pending")
    priority = Column(String(20), default="medium")
    user_id = Column(Integer,ForeignKey("users.id"))