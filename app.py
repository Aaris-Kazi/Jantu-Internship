from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"hello": "world"}

@app.get("/students")
def student_record(db: Session= Depends(get_db)):
    record = db.query(models.Students).all()
    return record

@app.get("/add_students/{name}")
def add_student(name:str, db: Session= Depends(get_db)):
    add = models.Students(name = name)
    db.add(add)
    db.commit()
    return "success"

# uvicorn app:app --reload