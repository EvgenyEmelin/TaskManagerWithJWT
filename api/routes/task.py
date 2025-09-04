from typing import List
from fastapi import APIRouter, HTTPException, Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.task import UserCreate, UserRead
from crud.task import create_task, read_tasks, read_task_by_id, update_task, delete_task, get_user_by_username, create_user
from schemas.task import TaskCreate, TaskRead
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_async_session
from database.models import User
from security.dependencies import get_current_user
from schemas.task import Token
from security.security import verify_password, create_access_token, hash_password
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta


router = APIRouter()

@router.post('/tasks/', response_model=TaskRead)
async def post_tasks(task_in: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = await create_task(task_in, session)
    return TaskRead.from_orm(task)

@router.get('/tasks/', response_model=List[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    tasks = await read_tasks(session)
    return [TaskRead.from_orm(task) for task in tasks]

@router.get('/tasks/{task_id}', response_model=TaskRead)
async def get_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await read_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskRead.from_orm(task)

@router.put('/tasks/{task_id}', response_model=TaskRead)
async def update_tasks(task_id: int, task_in: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = await update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Задача для обновления не найдена")
    return TaskRead.from_orm(task)

@router.delete('/tasks/{task_id}', response_model=TaskRead)
async def delete_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    task = await delete_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача для удаления не найдена")
    return TaskRead.from_orm(task)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    user = await get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model= UserRead)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    hashed_pw = hash_password(user_in.password)
    user = await create_user(db, user_in.username, user_in.email, hashed_pw)
    return user