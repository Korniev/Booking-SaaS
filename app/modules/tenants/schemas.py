import uuid
from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    slug: str


class TenantRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    is_active: bool

    class Config:
        from_attributes = True