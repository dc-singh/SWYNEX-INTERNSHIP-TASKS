from fastapi import APIRouter
from src.controller import controller



user_routes = APIRouter(prefix="/users", tags=["Users"])



@user_routes.get("/")
def get_users():
    return controller.read_local_json()