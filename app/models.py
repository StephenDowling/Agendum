from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)

    folders: List["Folder"] = Relationship(back_populates="user")


class Folder(SQLModel, table=True):
    __tablename__ = "folders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str

    user: Optional[User] = Relationship(back_populates="folders")
    notes: List["Note"] = Relationship(back_populates="folder")

class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    folder_id: Optional[int] = Field(default=None, foreign_key="folders.id")
    title: str
    content: str
    completed: bool = Field(default=False)
    priority: int = Field(default=0)
    created: date = Field(default_factory=lambda:datetime.utcnow().date())  
    due: Optional[date] = None

    folder: Optional[Folder] = Relationship(back_populates="notes")