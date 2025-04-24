from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "sqlite:///todos.db",
    connect_args={"check_same_thread": False}
)
Base = declarative_base()

class TodoDB(Base):
    __tablename__ = "todos"
    
    id = Column(Integer,primary_key=True,)
    title = Column(String,nullable=False)
    amount = Column(Integer,default=1)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)