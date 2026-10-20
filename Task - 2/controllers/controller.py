from models.models import User
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schema.schemas import UserSchema




def get_user(body: UserSchema, db:Session, user:User):
    user = db.get(User)
    return user
    # pass