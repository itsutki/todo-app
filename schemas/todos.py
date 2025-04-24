from pydantic import BaseModel
from typing import Optional

class TodoResponse(BaseModel):
    id: int
    title: str
    amount: int
    completed: bool

    class Config:
        from_attributes=True

class TodoCreate(BaseModel):
    title: str
    amount: int

    class Config:
        from_attributes=True

class TodoUpdate(BaseModel):
    title: Optional[str]
    amount: Optional[int]

    class Config:
        from_attributes=True