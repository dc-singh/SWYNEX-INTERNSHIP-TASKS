from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from models import User, UserCreate, UserUpdate
from store import load_users, save_users


app = FastAPI(
    title="Swynex Users API",
    description="A documented CRUD API for managing users.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def authenticate(
    credential_id: Annotated[int, Header(alias="X-User-Id", ge=1)],
    credential_name: Annotated[str, Header(alias="X-User-Name", min_length=1, max_length=100)],
) -> dict:
    user = next(
        (
            candidate
            for candidate in load_users()
            if candidate["id"] == credential_id
            and candidate["name"].strip().casefold() == credential_name.strip().casefold()
        ),
        None,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
            headers={"WWW-Authenticate": "User-Id User-Name"},
        )
    permissions = ["read"]
    if user["age"] >= 18:
        permissions.append("write")
    return {**user, "permissions": permissions}


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={"error": {"code": f"HTTP_{exc.status_code}", "message": str(exc.detail)}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": jsonable_encoder(exc.errors()),
            }
        },
    )


@app.get("/", tags=["General"])
def root():
    return {"message": "Swynex Users API is running"}


@app.get("/health", tags=["General"])
def health():
    return {"status": "healthy"}


@app.post("/api/authenticate", tags=["Authentication"])
def authenticate_endpoint(user: Annotated[dict, Depends(authenticate)]):
    return {"message": "Authentication successful", "user": user}


@app.get("/api/users", tags=["Users"])
def list_users(
    user: Annotated[dict, Depends(authenticate)],
    search: str | None = Query(default=None, max_length=100),
):
    if "read" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: read")
    users = load_users()
    if search:
        needle = search.strip().casefold()
        users = [item for item in users if needle in item["name"].casefold()]
    return {"count": len(users), "users": users}


@app.get("/api/users/{user_id}", response_model=User, tags=["Users"])
def get_user(
    user_id: Annotated[int, Path(ge=1)],
    user: Annotated[dict, Depends(authenticate)],
):
    if "read" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: read")
    if user_id < 1:
        raise HTTPException(status_code=400, detail="Id must be a positive integer")
    user = next((item for item in load_users() if item["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/users", status_code=201, response_model=User, tags=["Users"])
def create_user(
    data: UserCreate,
    user: Annotated[dict, Depends(authenticate)],
):
    if "write" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: write")
    users = load_users()
    user_id = max((item["id"] for item in users), default=0) + 1
    user = {"id": user_id, **data.model_dump()}
    users.append(user)
    save_users(users)
    return user


@app.put("/api/users/{user_id}", response_model=User, tags=["Users"])
def replace_user(
    user_id: Annotated[int, Path(ge=1)],
    data: UserCreate,
    user: Annotated[dict, Depends(authenticate)],
):
    if "write" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: write")
    users = load_users()
    for index, current in enumerate(users):
        if current["id"] == user_id:
            updated = {"id": user_id, **data.model_dump()}
            users[index] = updated
            save_users(users)
            return updated
    raise HTTPException(status_code=404, detail="User not found")


@app.patch("/api/users/{user_id}", response_model=User, tags=["Users"])
def update_user(
    user_id: Annotated[int, Path(ge=1)],
    data: UserUpdate,
    user: Annotated[dict, Depends(authenticate)],
):
    if "write" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: write")
    changes = data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=422, detail="At least one field must be provided")
    users = load_users()
    for index, current in enumerate(users):
        if current["id"] == user_id:
            updated = {**current, **changes}
            users[index] = updated
            save_users(users)
            return updated
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/api/users/{user_id}", status_code=200, tags=["Users"])
def delete_user(
    user_id: Annotated[int, Path(ge=1)],
    user: Annotated[dict, Depends(authenticate)],
):
    if "write" not in user["permissions"]:
        raise HTTPException(status_code=403, detail="Permission required: write")
    users = load_users()
    for index, current in enumerate(users):
        if current["id"] == user_id:
            deleted = users.pop(index)
            save_users(users)
            return {"message": "User deleted successfully", "user": deleted}
    raise HTTPException(status_code=404, detail="User not found")
