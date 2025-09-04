from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Создаем асинхронный движок с SQLite
engine = create_async_engine("sqlite+aiosqlite:///./database.db", echo=True)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Функция-зависимость для FastAPI, выдающая сессию
async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
