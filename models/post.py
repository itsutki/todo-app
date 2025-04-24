from pydantic import BaseModel
from typing import Optional

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