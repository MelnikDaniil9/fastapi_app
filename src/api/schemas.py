from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    age: int
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class CreateProfile(schemas.BaseModel):
    title: str
    description: str
    profession: str


class ReadProfile(schemas.BaseModel):
    title: str
    description: str
    avatar_url: str
    profession: str
    user_id: int


class UpdateProfile(schemas.BaseModel):
    title: str
    description: str
    profession: str
