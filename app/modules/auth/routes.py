import logging

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from redis import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import db_session, get_password_hasher
from app.core.exceptions import TooManyRequestsError
from app.core.security import PasswordHasher
from app.infra.db.models.user import User
from app.infra.redis.client import get_redis
from app.modules.auth.dependencies import require_active_user
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRead

logger = logging.getLogger("app.auth")

router = APIRouter(prefix="/auth", tags=["auth"])


def get_users_repo() -> UserRepository:
    return UserRepository()


def get_auth_service(
    users_repo: UserRepository = Depends(get_users_repo),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(users_repo, hasher)


async def check_login_rate_limit(
    request: Request,
    redis: aioredis.Redis = Depends(get_redis),
) -> None:
    ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:login:{ip}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, settings.rate_limit_login_window)
        if count > settings.rate_limit_login_max:
            raise TooManyRequestsError(
                f"Too many login attempts. Try again in {settings.rate_limit_login_window} seconds."
            )
    except RedisError as e:
        logger.warning("Rate limit check failed for ip=%s: %s", ip, e)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_session),
    service: AuthService = Depends(get_auth_service),
    _: None = Depends(check_login_rate_limit),
):
    token = await service.login(session, email=form.username, password=form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(require_active_user)):
    return user
