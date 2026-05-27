import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.models.resource import Resource


class ResourceRepository:
    async def get(self, session: AsyncSession, resource_id: uuid.UUID, tenant_id: uuid.UUID) -> Resource | None:
        res = await session.execute(
            select(Resource).where(Resource.id == resource_id, Resource.tenant_id == tenant_id)
        )
        return res.scalar_one_or_none()

    async def list(self, session: AsyncSession, tenant_id: uuid.UUID) -> list[Resource]:
        res = await session.execute(
            select(Resource).where(Resource.tenant_id == tenant_id, Resource.is_active.is_(True))
        )
        return list(res.scalars().all())

    async def create(self, session: AsyncSession, resource: Resource) -> Resource:
        session.add(resource)
        await session.commit()
        await session.refresh(resource)
        return resource