from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.models.tenant import Tenant


class TenantRepository:
    async def get_by_slug(self, session: AsyncSession, slug: str) -> Tenant | None:
        res = await session.execute(select(Tenant).where(Tenant.slug == slug))
        return res.scalar_one_or_none()

    async def create(self, session: AsyncSession, tenant: Tenant) -> Tenant:
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)
        return tenant