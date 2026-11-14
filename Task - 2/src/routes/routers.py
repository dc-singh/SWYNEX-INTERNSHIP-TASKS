from fastapi import APIRouter, HTTPException
from src.utility.utils import load_json, save_file
from src.controller.controller import one_user, delete_user as delete_user_by_id
from src.schemas.schemas import User, UpdatedUser



user_routes = APIRouter(prefix="/api/users", tags=["Users"])



@user_routes.get("/")
def get_users():
    return load_json()

@user_routes.get("/{id}")
def get_single_user(id: int=0):
    return one_user(id)

@user_routes.post("/create_users")
def create_user(data: User):
    user = load_json()
    
    next_id = max([u["id"] for u in user]) + 1 if user else 1
    new_user = data.model_dump()
    new_user["id"] = next_id
    user.append(new_user)
    save_file(user)
    return {"message": "User created successfully"}


@user_routes.delete("/delete_user")
def delete_user(id: int):
    return delete_user_by_id(id)


@user_routes.put("/update_user/{id}")
def update_user(data: UpdatedUser, id: int):
    allUsers = load_json()

    if not id:
        raise HTTPException(status_code=404, detail="Id not found")

    for index, users in enumerate(allUsers):
        if users["id"] == id:
            changes = {}
            for k, v in users.model_dump().items():
                if v is not None:
                    changes[k] = v

            allUsers[index] = {"id":id, **users, **changes}

            save_file(allUsers)
            return {"message":"user updated successfully"}
        raise HTTPException(status_code=400, detail="user not found")