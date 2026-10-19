from fastapi import FastAPI
from db import database
from models import User



user_routes = FastAPI(prefix="/api/v1")

@user_routes.get("/users")
def get_users():
    query = User.select()
    return database.fetch_all(query)