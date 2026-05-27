import uuid
from datetime import datetime
from pydantic import BaseModel


class BookingCreate(BaseModel):
    resource_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    notes: str | None = None


class BookingRead(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    resource_id: uuid.UUID
    user_id: uuid.UUID
    start_at: datetime
    end_at: datetime
    status: str
    notes: str | None

    class Config:
        from_attributes = True