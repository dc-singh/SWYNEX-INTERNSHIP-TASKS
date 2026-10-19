from fastapi import FastAPI
from db import database
from routers.router import user_routes
from models import User


app = FastAPI()


@app.get("/")
def root():
    return {"Message": "Backend Server Successfully Started"}