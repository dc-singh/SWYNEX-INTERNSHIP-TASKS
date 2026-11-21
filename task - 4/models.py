from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_name(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Name must not be blank")
    return value


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)

    _normalize_name = field_validator("name")(normalize_name)


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=120)

    _normalize_name = field_validator("name")(normalize_name)


class User(BaseModel):
    id: int
    name: str
    age: int
