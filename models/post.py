from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    amount: int

    class Config:
        from_attributes=True
