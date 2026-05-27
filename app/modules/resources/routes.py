import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import db_session
from app.infra.db.models.tenant import Tenant
from app.infra.db.models.user import User
from app.infra.redis.cache import cache_delete, cache_get, cache_set
from app.infra.redis.client import get_redis
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
    redis: aioredis.Redis = Depends(get_redis),
):
    resource = await service.create(session, tenant, payload)
    await cache_delete(redis, f"resources:{tenant.slug}")
    return resource


@router.get("", response_model=list[ResourceRead])
async def list_resources(
    session: AsyncSession = Depends(db_session),
    tenant: Tenant = Depends(require_tenant),
    _: User = Depends(require_active_user),
    service: ResourceService = Depends(get_resource_service),
    redis: aioredis.Redis = Depends(get_redis),
):
    cache_key = f"resources:{tenant.slug}"
    cached = await cache_get(redis, cache_key)
    if cached is not None:
        return cached

    resources = await service.list(session, tenant)
    serialized = [ResourceRead.model_validate(r).model_dump(mode="json") for r in resources]
    await cache_set(redis, cache_key, serialized, ttl=settings.cache_resources_ttl)
    return resources
