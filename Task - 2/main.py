from fastapi import FastAPI
from src.routes.routes import user_routes


app = FastAPI()

app.include_router(user_routes)


@app.get("/")
def home():
    return {"Message":"Application is running"}