from fastapi import APIRouter
from src.utility.utils import load_json
from src.controller.controller import one_user, CreateUser
from src.schemas.schemas import User



user_routes = APIRouter(prefix="/api/users", tags=["Users"])



@user_routes.get("/")
def get_users():
    return load_json()

@user_routes.get("/{id}")
def get_single_user(id: int=0):
    return one_user(id)

@user_routes.post("/create_users")
def create_user(data: User):
    pass