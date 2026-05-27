from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.infra.db.models.tenant import Tenant
from app.infra.db.models.user import User
from app.modules.auth.dependencies import require_active_user
from app.modules.resources.dependencies import get_resource_service
from app.modules.resources.schemas import ResourceCreate, ResourceRead
from app.modules.resources.service import ResourceService
from app.modules.tenants.dependencies import require_tenant

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    payload: ResourceCreate,
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    _: User = Depends(require_active_user),
    service: ResourceService = Depends(get_resource_service),
):
    return await service.create(session, tenant, payload)


@router.get("", response_model=list[ResourceRead])
async def list_resources(
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    _: User = Depends(require_active_user),
    service: ResourceService = Depends(get_resource_service),
):
    return await service.list(session, tenant)