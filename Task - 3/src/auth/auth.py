from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from src.utility.utils import load_json


READ_PERMISSION = "read"
WRITE_PERMISSION = "write"


def authenticate_user(
    user_id: Annotated[int, Header(alias="X-User-Id", ge=1)],
    user_name: Annotated[str, Header(alias="X-User-Name", min_length=1, max_length=100)],
) -> dict:
    """Authenticate a user against the users stored in data.json.

    The data source has no password or role fields, so the existing id/name
    pair is used as the identity credential. Adults are granted write access;
    every authenticated user is granted read access.
    """
    normalized_name = user_name.strip().casefold()
    if not normalized_name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
            headers={"WWW-Authenticate": "User-Id User-Name"},
        )
    user = next(
        (
            candidate
            for candidate in load_json()
            if candidate.get("id") == user_id
            and candidate.get("name", "").strip().casefold() == normalized_name
        ),
        None,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
            headers={"WWW-Authenticate": "User-Id User-Name"},
        )

    permissions = [READ_PERMISSION]
    if user["age"] >= 18:
        permissions.append(WRITE_PERMISSION)

    return {**user, "permissions": permissions}


def require_permission(permission: str):
    def permission_checker(
        user: Annotated[dict, Depends(authenticate_user)],
    ) -> dict:
        if permission not in user["permissions"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}",
            )
        return user

    return permission_checker
