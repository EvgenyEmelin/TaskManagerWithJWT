#Файл создание ORM моделей
from sqlalchemy.orm import Mapped, mapped_column
from .session import Base

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default='new')
    priority: Mapped[int] = mapped_column(default=1)
    date_of_end: Mapped[str] = mapped_column(nullable=True)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(index=True, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
