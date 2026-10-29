from fastapi import APIRouter
from src.utility.utils import load_json



user_routes = APIRouter(prefix="/users", tags=["Users"])



@user_routes.get("/")
def get_users():
    return load_json()