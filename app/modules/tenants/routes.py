from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.infra.db.models.user import User
from app.modules.auth.dependencies import require_superuser
from app.modules.tenants.dependencies import get_tenant_service
from app.modules.tenants.schemas import TenantCreate, TenantRead
from app.modules.tenants.service import TenantService

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    payload: TenantCreate,
    session: AsyncSession = Depends(db_session),
    service: TenantService = Depends(get_tenant_service),
    _: User = Depends(require_superuser),
):
    return await service.create(session, payload)