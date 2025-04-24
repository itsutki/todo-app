from pydantic import BaseModel

class TodoResponse(BaseModel):
    id: int
    title: str
    amount: int
    completed: bool

    class Config:
        from_attributes=True