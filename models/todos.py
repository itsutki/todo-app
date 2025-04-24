from sqlalchemy import Column, String, Integer, Boolean
from database import Base

class TodoDB(Base):
    __tablename__ = "todos"
    
    id = Column(Integer,primary_key=True,)
    title = Column(String,nullable=False)
    amount = Column(Integer,default=1)
    completed = Column(Boolean, default=False)
