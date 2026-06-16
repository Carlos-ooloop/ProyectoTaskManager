from sqlalchemy import Column,Integer,String
from db.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
    __tablename__ = "users"
    
    id = Column( Integer, primary_key=True,index=True)
    username : Mapped[str] = mapped_column(String(50), unique=True)
    email : Mapped[str] = mapped_column(String(50), unique=True)
    password :Mapped[str] = mapped_column(String(255))
    role : Mapped[str] = mapped_column(String(20), default="user")
    
    tasks = relationship("Task", back_populates= "owner")   