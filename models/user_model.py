from sqlalchemy import Column,Integer,String
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column( Integer, primary_key=True,index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(255))
    role = Column(String(20), default="user")
    
    tasks = relationship("Task", back_populates= "owner")   