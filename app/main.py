from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel, Field
from datetime import date
from enum import IntEnum
import psycopg
from psycopg.rows import dict_row
import time
from sqlmodel import SQLModel, Session, select
from app.database import engine, create_db_and_tables, get_session
from app import models   
from app.models import Note
from app.schemas import NoteCreate        

SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# enum for priority
class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

# root
@app.get("/")
async def root():
    return {"message" : "Hello World!"}

# get all notes
@app.get("/notes")
def get_notes(session: Session = Depends(get_session)):
    statement = select(Note) #SQL query object named statement, doesn't run it just defines it 
    results = session.exec(statement) #executes statement 
    return results.all()

# create a note
@app.post("/notes", status_code=status.HTTP_201_CREATED) #doesnt use session.query() because we're not querying, we are creating a new row and inserting 
def create_note(note_in: NoteCreate, session: Session = Depends(get_session)):
    note = Note(**note_in.model_dump()) #constructs model instance from Pydantic data, dump() turns it into a dictionary
    session.add(note) #SQLAlchemy method for adding 
    session.commit()
    session.refresh(note)
    return note

# get note by ID
@app.get("/notes/{id}")
def get_note(id : int, response : Response, session: Session = Depends(get_session)):
    statement = select(Note).where(Note.id == id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail = f"note with ID of {id} was not found")
    return result 

# delete a note 
@app.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, session: Session = Depends(get_session)):
    statement = select(Note).where(Note.id == id)
    note = session.exec(statement).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a note 
@app.put("/notes/{id}")
def update_note(id: int, note_data: NoteCreate, session: Session = Depends(get_session)):
    statement = select(Note).where(Note.id == id)
    existing_note = session.exec(statement).first()

    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update fields manually
    existing_note.folder_id = note_data.folder_id
    existing_note.title = note_data.title
    existing_note.content = note_data.content
    existing_note.completed = note_data.completed
    existing_note.priority = note_data.priority
    existing_note.due = note_data.due

    session.add(existing_note)
    session.commit()
    session.refresh(existing_note)

    return existing_note