from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserRead(UserBase):
    id: UUID

    class Config:
        from_attributes = True



class UserRoleUpdate(BaseModel):
    is_superuser: bool

class UserActiveUpdate(BaseModel):
    is_active: bool


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str