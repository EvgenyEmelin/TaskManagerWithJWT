from datetime import datetime
from pydantic import BaseModel, EmailStr
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

#Модели для JWT Токена

class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    username: Optional[str]  = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }