import uuid
from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.CreateUpdateDictModel):
    id: uuid.UUID
    email: EmailStr


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserUpdate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str
