from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from datetime import date
from enum import IntEnum
import psycopg
from psycopg.rows import dict_row
import time


app = FastAPI()


# enum for priority
class Priority(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

# defines what a note is and should look like
class Note(BaseModel):
    folder_id: int
    title: str
    content: str
    completed: Optional[bool] = False
    priority: Optional[Priority] = Priority.LOW  #default value
    created: date = Field(default_factory=date.today)
    due: Optional[date] = Field(default_factory=date.today)

while True:
    try:
        conn = psycopg.connect(
            host='localhost',
            dbname='Agendum', 
            user='postgres',
            password='password', 
            row_factory=dict_row 
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed :(")
        print("Error:", error)
        time.sleep(2) # keep trying to connect to database every 2 seconds 
    
my_notes = [{
    "title": "To Do list",
    "content": "Take out the bins\nFeed the dogs\nGo for a walk",
    "completed": False,
    "priority": 0,
    "created": "2025-06-30",
    "due": "2025-07-01",
    "id": 1
},
{
    "title": "Shopping List",
    "content": "Bread\nMilk\nButter",
    "completed": False,
    "priority": 1,
    "created": "2025-06-30",
    "due": "2025-07-01",
    "id": 2
}]

print(my_notes)

# helper method for getting note by ID
def find_note(id):
    for i in my_notes:
        if i["id"] == id:
            return i  
        
# helper method for finding index of a note using ID
def find_index_note(id: int):
    for index, note in enumerate(my_notes):
        if note['id'] == id:
            return index
    return None

# root
@app.get("/")
async def root():
    return {"message" : "Hello World!"}

# get all notes
@app.get("/notes")
def get_notes():
    cursor.execute("""SELECT * FROM notes""")
    notes = cursor.fetchall()
    return {"data" : notes}

# create a note
@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(note: Note):
    cursor.execute("""INSERT INTO notes (folder_id, title, content, completed, priority, due) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""", (note.folder_id, note.title, note.content, note.completed, note.priority.value, note.due))
    new_note = cursor.fetchone()
    conn.commit()
    return {"data" : new_note} 

# get note by ID
@app.get("/notes/{id}")
def get_note(id : int, response : Response):
    cursor.execute("""SELECT * FROM notes WHERE id = %s""", (id,)) #have to add , after as it's treated a tuple 
    note = cursor.fetchone()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"note with ID of {id} was not found")
    return {"data" : note}

# delete a note 
@app.delete("/notes/{id}")
def delete_note(id: int, response : Response):
    cursor.execute("""DELETE FROM notes WHERE id = %s RETURNING *""", (id,))
    note = cursor.fetchone()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a note 
@app.put("/notes/{id}")
def update_note(id: int, response : Response, note: Note):
    cursor.execute("""UPDATE notes SET folder_id = %s, title = %s, content =%s, completed =%s, priority = %s, due = %s WHERE id = %s RETURNING *""", (note.folder_id, note.title, note.content, note.completed, note.priority.value, note.due, id,))
    note = cursor.fetchone()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    conn.commit()
    return {"data" : note}