from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI(docs_url="/doc")
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    uName: str
    uEmail: str
    uId: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{id}", status_code=status.HTTP_200_OK)
async def read_user(id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


@app.get("/users", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    users = db.query(models.User).all()
    return users


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return


@app.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, user_update: UserBase, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.uName = user_update.uName
    user.uEmail = user_update.uEmail
    user.uId = user_update.uId
    db.commit()
    db.refresh(user)
    return user


@app.get("/query")
def query_fun(name: str, roll: int):
    ver_name = {"name": name, "roll": roll}
    return ver_name
