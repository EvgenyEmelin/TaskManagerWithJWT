from fastapi import FastAPI
from api.routes.task import router as task_router
import asyncio
from database.session import engine, Base

app = FastAPI()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

if __name__ == "__main__":
    asyncio.run(init_models())
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
