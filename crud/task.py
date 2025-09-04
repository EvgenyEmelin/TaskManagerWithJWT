from typing import List, Optional
from schemas.task import TaskCreate, TaskRead
from database.models import Task, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_task(task: TaskCreate, database: AsyncSession) -> Task:
    task = Task(
        title = task.title,
        description = task.description,
        status = task.status,
        priority = task.priority,
        date_of_end = task.date_of_end
    )
    database.add(task)
    await database.commit()
    await database.refresh(task)
    return task

async def read_tasks(database: AsyncSession) -> List[Task]:
    query = select(Task)
    result = await database.execute(query)
    tasks = result.scalars().all()
    return tasks

async def read_task_by_id(database: AsyncSession, task_id:int) -> Task | None:
    query = await database.get(Task, task_id)
    return query

async def update_task(database: AsyncSession,task_id: int, data_update: TaskCreate) -> Optional[Task]:
    query = await database.get(Task, task_id)
    if not query:
        return None
    update_data = data_update.dict(exclude_none=True)
    for field, value in update_data.items():
        setattr(query, field, value)
    database.add(query)
    await database.commit()
    await database.refresh(query)
    return query

async def delete_task(database: AsyncSession, task_id: int) -> Optional[Task]:
    query = await database.execute(select(Task).filter(Task.id == task_id))
    task = query.scalars().first()
    if not task:
        return None
    await database.delete(task)
    await database.commit()
    return task

async def get_user_by_username(database: AsyncSession, username: str) -> User | None:
    result = await database.execute(select(User).where(User.username == username))
    return result.scalars().first()