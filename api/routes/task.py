from typing import List
from fastapi import APIRouter, HTTPException, Depends
from crud.task import create_task, read_tasks, read_task_by_id, update_task, delete_task
from schemas.task import TaskCreate, TaskRead
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_async_session

router = APIRouter()

@router.post('/', response_model=TaskRead)
async def post_tasks(task_in: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = await create_task(task_in, session)
    return TaskRead.from_orm(task)

@router.get('/', response_model=List[TaskRead])
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    tasks = await read_tasks(session)
    return [TaskRead.from_orm(task) for task in tasks]

@router.get('/{task_id}', response_model=TaskRead)
async def get_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await read_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskRead.from_orm(task)

@router.put('/{task_id}', response_model=TaskRead)
async def update_tasks(task_id: int, task_in: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = await update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Задача для обновления не найдена")
    return TaskRead.from_orm(task)

@router.delete('/{task_id}', response_model=TaskRead)
async def delete_task_by_id(task_id: int, session: AsyncSession = Depends(get_async_session)):
    task = await delete_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача для удаления не найдена")
    return TaskRead.from_orm(task)
