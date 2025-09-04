from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[str] = 'new'
    priority: Optional[int] = 1
    date_of_end: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True

class TaskRead(TaskCreate):
    id: int
