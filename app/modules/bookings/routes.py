import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.infra.db.models.tenant import Tenant
from app.infra.db.models.user import User
from app.modules.auth.dependencies import require_active_user
from app.modules.bookings.dependencies import get_booking_service
from app.modules.bookings.schemas import BookingCreate, BookingRead
from app.modules.bookings.service import BookingService
from app.modules.tenants.dependencies import require_tenant

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(
    payload: BookingCreate,
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    user: User = Depends(require_active_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.create(session, tenant, user, payload)


@router.post("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(
    booking_id: uuid.UUID,
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    user: User = Depends(require_active_user),
    service: BookingService = Depends(get_booking_service),
):
    return await service.cancel(session, tenant, user, booking_id)