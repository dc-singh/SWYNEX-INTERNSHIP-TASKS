from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from src.auth.auth import (
    READ_PERMISSION,
    WRITE_PERMISSION,
    require_permission,
)
from src.utility.utils import load_json, save_file
from src.controller.controller import one_user, delete_user as delete_user_by_id
from src.schemas.schemas import User, UpdatedUser



user_routes = APIRouter(prefix="/api/users", tags=["Users"])



@user_routes.get("/")
def get_users(
    _: Annotated[dict, Depends(require_permission(READ_PERMISSION))],
):
    return load_json()

@user_routes.get("/{id}")
def get_single_user(
    _: Annotated[dict, Depends(require_permission(READ_PERMISSION))],
    id: int = 0,
):
    user = one_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_routes.post("/create_users")
def create_user(
    data: User,
    _: Annotated[dict, Depends(require_permission(WRITE_PERMISSION))],
):
    user = load_json()
    
    next_id = max([u["id"] for u in user]) + 1 if user else 1
    new_user = data.model_dump()
    new_user["id"] = next_id
    user.append(new_user)
    save_file(user)
    return {"message": "User created successfully"}


@user_routes.delete("/delete_user")
def delete_user(
    id: int,
    _: Annotated[dict, Depends(require_permission(WRITE_PERMISSION))],
):
    return delete_user_by_id(id)


@user_routes.put("/update_user/{id}")
def update_user(
    data: UpdatedUser,
    id: int,
    _: Annotated[dict, Depends(require_permission(WRITE_PERMISSION))],
):
    allUsers = load_json()

    if id < 1:
        raise HTTPException(status_code=400, detail="Id must be a positive integer")

    for index, users in enumerate(allUsers):
        if users["id"] == id:
            changes = data.model_dump(exclude_unset=True)

            allUsers[index] = {"id":id, **users, **changes}

            save_file(allUsers)
            return {"message":"user updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")