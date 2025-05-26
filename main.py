from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from datetime import date


app = FastAPI()


# defines what a note is and should look like
class Note(BaseModel):
    created_date: date = Field(default_factory=date.today)
    title: str
    content: str
    completed: Optional[bool] = False

my_notes = [{
        "created_date" : "2025-05-24",
        "title" : "title of note 1",
        "content" : "content of note 1",
        "completed" : False,
        "id" : 1
    },
    {
        "created_date" : "2025-05-25",
        "title" : "title of note 2",
        "content" : "content of note 2",
        "completed" : True,
        "id" : 2
    }]

# helper method for getting post by ID
def find_note(id):
    for i in my_notes:
        if i["id"] == id:
            return i

# root
@app.get("/")
async def root():
    return {"message" : "Hello World!"}

# get all notes
@app.get("/notes")
def get_notes():
    return {"Data" : my_notes}

# create a note
@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(note: Note):
    note_dict = note.dict()
    note_dict['id'] = len(my_notes) + 1
    my_notes.append(note_dict)
    return {"message" : note_dict} 

# get note by ID
@app.get("/notes/{id}")
def get_note(id : int, response : Response):
    note = find_note(id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"note with ID of {id} was not found")
    return {"Data" : note}

