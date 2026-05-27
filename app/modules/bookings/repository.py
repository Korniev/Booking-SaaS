import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.models.booking import Booking


class BookingRepository:
    async def create(self, session: AsyncSession, booking: Booking) -> Booking:
        session.add(booking)
        await session.commit()
        await session.refresh(booking)
        return booking

    async def get(self, session: AsyncSession, booking_id: uuid.UUID, tenant_id: uuid.UUID) -> Booking | None:
        res = await session.execute(
            select(Booking).where(Booking.id == booking_id, Booking.tenant_id == tenant_id)
        )
        return res.scalar_one_or_none()