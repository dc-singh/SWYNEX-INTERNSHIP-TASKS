from fastapi import FastAPI
from src.routes.routers import user_routes


app = FastAPI()

app.include_router(user_routes)

@app.get("/")
def root():
    return {"Message":"Backend Server is Started Successfully"}