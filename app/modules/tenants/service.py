from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.infra.db.models.tenant import Tenant
from app.modules.tenants.repository import TenantRepository
from app.modules.tenants.schemas import TenantCreate


class TenantService:
    def __init__(self, repo: TenantRepository):
        self.repo = repo

    async def create(self, session: AsyncSession, data: TenantCreate) -> Tenant:
        existing = await self.repo.get_by_slug(session, data.slug)
        if existing:
            raise ConflictError("Tenant with this slug already exists")
        tenant = Tenant(name=data.name, slug=data.slug, is_active=True)
        return await self.repo.create(session, tenant)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Tenant:
        tenant = await self.repo.get_by_slug(session, slug)
        if not tenant:
            raise NotFoundError("Tenant not found")
        if not tenant.is_active:
            raise NotFoundError("Tenant inactive")
        return tenant