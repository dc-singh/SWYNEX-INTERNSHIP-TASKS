from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def validate_name(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("Name must not be blank")
    return normalized


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)

    _validate_name = field_validator("name")(validate_name)


class UpdatedUser(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=120)

    _validate_name = field_validator("name")(validate_name)

    @model_validator(mode="after")
    def require_update(self):
        if self.name is None and self.age is None:
            raise ValueError("At least one field must be provided")
        return self