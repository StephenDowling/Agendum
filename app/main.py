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

# delete a note 
@app.delete("/notes/{id}")
def delete_note(id: int, response : Response):
    index = find_index_note(id)
    if index is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    my_notes.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a note 
@app.put("/notes/{id}")
def update_note(id: int, response : Response, note: Note):
    index = find_index_note(id)
    if index is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note_dict = note.dict()
    note_dict['id'] = id
    my_notes[index] = note_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)