from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/Agendum'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#session dependency 
def get_session():
    with Session(engine) as session:
        yield session