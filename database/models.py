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