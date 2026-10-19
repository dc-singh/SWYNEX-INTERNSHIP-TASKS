from fastapi import APIRouter, Depends
from db import database
from models.models import User
from sqlalchemy.orm import Session


user_routes = APIRouter(prefix="/users", tags=["Users"])

@user_routes.get("/users")
def get_users(db: Session = Depends(database.get_db)):
    return db.query(User).all()