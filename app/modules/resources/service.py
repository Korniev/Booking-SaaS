from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.infra.db.models.resource import Resource
from app.infra.db.models.tenant import Tenant
from app.modules.resources.repository import ResourceRepository
from app.modules.resources.schemas import ResourceCreate


class ResourceService:
    def __init__(self, repo: ResourceRepository):
        self.repo = repo

    async def create(self, session: AsyncSession, tenant: Tenant, data: ResourceCreate) -> Resource:
        resource = Resource(
            tenant_id=tenant.id,
            name=data.name,
            description=data.description,
            timezone=data.timezone,
            capacity=data.capacity,
            is_active=True,
        )
        return await self.repo.create(session, resource)

    async def list(self, session: AsyncSession, tenant: Tenant) -> list[Resource]:
        return await self.repo.list(session, tenant.id)

    async def get(self, session: AsyncSession, tenant: Tenant, resource_id) -> Resource:
        r = await self.repo.get(session, resource_id, tenant.id)
        if not r:
            raise NotFoundError("Resource not found")
        if not r.is_active:
            raise NotFoundError("Resource inactive")
        return r