from sqlalchemy import Boolean, Column, Integer, String
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default="No description")
    dateTime = Column(String)
    completed = Column(Boolean, default=False)