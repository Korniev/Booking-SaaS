import uuid

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import db_session
from app.infra.db.models.tenant import Tenant
from app.infra.db.models.user import User
from app.infra.redis.cache import cache_get, cache_set
from app.infra.redis.client import get_redis
from app.modules.auth.dependencies import require_active_user
from app.modules.bookings.dependencies import get_booking_service
from app.modules.bookings.schemas import BookingCreate, BookingRead
from app.modules.bookings.service import BookingService
from app.modules.tenants.dependencies import require_tenant

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate,
    response: Response,
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    user: User = Depends(require_active_user),
    service: BookingService = Depends(get_booking_service),
    redis: aioredis.Redis = Depends(get_redis),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    if idempotency_key is not None:
        cached = await cache_get(redis, f"idempotency:{idempotency_key}")
        if cached is not None:
            response.status_code = status.HTTP_200_OK
            return cached

    booking = await service.create(session, tenant, user, payload)

    if idempotency_key is not None:
        booking_data = BookingRead.model_validate(booking).model_dump(mode="json")
        await cache_set(redis, f"idempotency:{idempotency_key}", booking_data, ttl=settings.idempotency_ttl)

    return booking


@router.post("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(
    booking_id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    user: User = Depends(require_active_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.cancel(session, tenant, user, booking_id)
