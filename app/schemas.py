from sqlmodel import SQLModel
from typing import Optional
from datetime import date

class NoteCreate(SQLModel):
    folder_id: int
    title: str
    content: str
    completed: bool = False
    priority: int = 0
    due: Optional[date] = None  

    class Config:
        from_attributes = True  
    
