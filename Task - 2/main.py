from fastapi import FastAPI
from db import database
from routers.router import user_routes
# from models import User


app = FastAPI()
app.include_router(user_routes)


@app.get("/")
def root():
    return {"Message": "Backend Server Successfully Started"}


@app.get("/health")
def health():
    return {"Message": "Backend Server is Healthy"}