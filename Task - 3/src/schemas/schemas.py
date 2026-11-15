from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int

class UpdatedUser(BaseModel):
    name:str = None
    age: int = None