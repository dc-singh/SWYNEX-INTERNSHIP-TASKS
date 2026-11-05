from src.utility.utils import load_json
from src.schemas.schemas import User


def one_user(id: int):
    data = load_json()
    for user in data:
        if user["id"] == id:
            return user
    return None

