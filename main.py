from fastapi import FastAPI, Depends, HTTPException, status
from services.auth import get_password_hash
from schemas.todos import TodoCreate, TodoUpdate, TodoResponse
from schemas.users import UserCreate, UserResponse
from models.todos import TodoDB
from models.users import UserDB
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
def get_db(): #different sessions for each request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register",
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Register a new user"
          )
async def create_user(user: UserCreate, db:Session = Depends(get_db)):
    """
    Create a new user with a unique username and hashed password.
    """
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    new_user = UserDB(username = user.username, hashed_password = hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo not found") #raise http error if query returns no todo item for the given id
    return todo_item

@app.get("/", response_model=List[TodoResponse]) # dif. response model for id and completed
async def read_todos(db: Session = Depends(get_db)): # dif. sessions for every request
    todo_item = db.query(TodoDB).all()
    return todo_item

@app.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id:int, item:TodoUpdate, db: Session = Depends(get_db)):
    todo_item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo ID not found")
    todo_item.title = item.title
    todo_item.amount = item.amount
    db.commit()
    db.refresh(todo_item)
    return todo_item

@app.post("/", response_model=TodoResponse)
async def create_item(item: TodoCreate, db: Session = Depends(get_db)): #Todo: post req. model
    item = TodoDB(title = item.title, amount = item.amount) #Todos db model
    db.add(item)
    db.commit()
    db.refresh(item) #  Always refresh → best practice.
    return item

@app.delete("/{todo_id}")
async def delete_item(todo_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(item)
    db.commit()
    return {"message": f"Todo number {todo_id} is deleted successfully."}
