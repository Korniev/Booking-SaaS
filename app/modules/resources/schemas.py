import uuid
from pydantic import BaseModel


class ResourceCreate(BaseModel):
    name: str
    description: str | None = None
    timezone: str = "UTC"
    capacity: int = 1


class ResourceRead(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: str | None
    timezone: str
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True