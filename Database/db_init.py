from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from Database.db_properties import Base


class DatabaseTodo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225))
    description = Column(String(225), nullable=True)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class DatabaseUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(225), unique=True, index=True)
    username = Column(String(225), unique=True, index=True)
    first_name = Column(String(225))
    last_name = Column(String(225))
    hashed_password = Column(String(225))
    is_active = Column(Boolean, default=True)

    todos = relationship("DatabaseTodo")
