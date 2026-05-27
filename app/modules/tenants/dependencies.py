from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.core.exceptions import BadRequestError
from app.infra.db.models.tenant import Tenant
from app.modules.tenants.repository import TenantRepository
from app.modules.tenants.service import TenantService


def get_tenant_repo() -> TenantRepository:
    return TenantRepository()


def get_tenant_service(repo: TenantRepository = Depends(get_tenant_repo)) -> TenantService:
    return TenantService(repo)


async def require_tenant(
    session: AsyncSession = Depends(db_session),
    service: TenantService = Depends(get_tenant_service),
    x_tenant: str | None = Header(default=None, alias="X-Tenant"),
) -> Tenant:
    if not x_tenant:
        raise BadRequestError("Missing X-Tenant header")
    return await service.get_by_slug(session, x_tenant)