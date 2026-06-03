import uuid
from pydantic import BaseModel, ConfigDict


class TenantCreate(BaseModel):
    name: str
    slug: str


class TenantRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)