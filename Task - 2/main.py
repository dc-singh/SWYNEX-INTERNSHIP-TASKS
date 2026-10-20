from fastapi import FastAPI
from db import database
from routers.router import router
# from models import User


app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"Message": "Backend Server Successfully Started"}


@app.get("/health")
def health():
    return {"Message": "Backend Server is Healthy"}