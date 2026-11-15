from fastapi import Depends, FastAPI

from src.auth.auth import authenticate_user
from src.routes.routers import user_routes


app = FastAPI()
app.include_router(user_routes)


@app.post("/api/authenticate")
def authenticate(
    user: dict = Depends(authenticate_user),
):
    return {
        "message": "Authentication successful",
        "user": user,
    }
