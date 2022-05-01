from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import update, select

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
        add = models.Students(student_name = name)
        db.add(add)
        db.commit()
        return "success"
    except Exception as e:
        return "Issue occured "+e

@app.get("/books")
def student_record(db: Session= Depends(get_db)):
    record = db.query(models.Books).all()
    return record

@app.get("/add_books/{name}")
def add_student(name:str, db: Session= Depends(get_db)):
    try:
        add = models.Books(name = name)
        db.add(add)
        db.commit()
        return "success"
    except Exception as e:
        return "Issue occured "+e



@app.get("/inventory")
def student_record(db: Session= Depends(get_db)):
    record = db.query(models.Inventory).all()
    return record

@app.get("/update_books/{b_name}")
def student_record(b_name,  db: Session= Depends(get_db)):
    upd = update(models.Books)
    u = upd.values({"available": 1})
    u = u.where(models.Books.name == b_name)
    engine.execute(u)
    return "success"

@app.get("/select")
def student_record(db: Session= Depends(get_db)):
    sel = select(models.Students.id).where(models.Students.student_name == "Aaris")
    res = engine.execute(sel)
    res =res.fetchone()
    print(res)
    return res

def book_update(b_name, val):
    upd = update(models.Books)
    u = upd.values({"available": val})
    u = u.where(models.Books.name == b_name)
    engine.execute(u)
    return "success"

def invent_update(s_name, b_name, val):
    upd = update(models.Inventory)
    u = upd.values({"returned": val})
    u = u.where(models.Inventory.student_name == s_name and models.Inventory.Book_name == b_name)
    engine.execute(u)
    return "success"

def book_stat(book_name):
    sel = select(models.Books.available).where(models.Books.name == book_name)
    res = engine.execute(sel)
    res =res.fetchone()
    return res

def book_count(book_name,db: Session= Depends(get_db)):
    sel = select(models.Books.name).where(models.Books.name == book_name)
    # sel = db.query(models.Books.name == book_name).count()
    res = engine.execute(sel)
    data = [i for i in res]
    # res  =res.fetchone()
    return data

    
@app.get("/issue_books/{s_name}/{b_name}")
def issue_books(s_name:str, b_name:str, db: Session= Depends(get_db)):
    s =book_count(b_name)
    print(len(s))
    if len(s) == 0:
        print('Book Does not Exist')
        return 'Book Does not Exist'
    else:
        res = book_stat(b_name)
        # print(res,  type(res))
        res = str(res)
        if res == '(True,)':
            try:
                print(s_name, b_name)
                book_update(b_name, 0)
                add = models.Inventory(student_name = s_name, Book_name= b_name, returned = 0)
                db.add(add)
                db.commit()
                return "success"
            except Exception as e:
                e
            print('true')
        else:
            print('false')
            return "Book already issued"
    
@app.get("/return_books/{s_name}/{b_name}")
def return_books(s_name:str, b_name:str, db: Session= Depends(get_db)):
    res = book_stat(b_name)
    res = str(res)
    if res != '(True,)':
        print('')
        book_update(b_name, 1)
        invent_update(s_name, b_name, 1)
        return "Success"
    else:
        return "Book not issued"
    

@app.get("/drop")
def student_record(db: Session= Depends(get_db)):
    models.Inventory.__table__.drop(engine)
    return 'success'


# uvicorn app:app --reload