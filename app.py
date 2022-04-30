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
    try:
        add = models.Students(name = name)
        db.add(add)
        db.commit()
        return "success"
    except Exception as e:
        return "Issue occured "+e

@app.get("/add_books/{name}")
def add_student(name:str, db: Session= Depends(get_db)):
    try:
        add = models.Books(name = name)
        db.add(add)
        db.commit()
        return "success"
    except Exception as e:
        return "Issue occured "+e


@app.get("/books")
def student_record(db: Session= Depends(get_db)):
    record = db.query(models.Books).all()
    return record

@app.get("/managemnt")
def student_record(db: Session= Depends(get_db)):
    record = db.query(models.Managements).all()
    return record


# uvicorn app:app --reload