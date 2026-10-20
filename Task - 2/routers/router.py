from fastapi import APIRouter, Depends
from db import database
from models.models import User
from sqlalchemy.orm import Session
from controllers import controller


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    return database.controller.get(User)