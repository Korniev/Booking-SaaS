import uuid
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session, get_password_hasher
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_token, PasswordHasher
from app.infra.db.models.user import User
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_users_repo() -> UserRepository:
    return UserRepository()


def get_auth_service(
    users_repo: UserRepository = Depends(get_users_repo),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(users_repo, hasher)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_session),
    repo: UserRepository = Depends(get_users_repo),
) -> User:
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("Invalid token")
        user_id = uuid.UUID(sub)
    except Exception:
        raise UnauthorizedError("Invalid token")

    user = await repo.get_by_id(session, user_id)
    if not user:
        raise UnauthorizedError("User not found")
    return user


def require_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise ForbiddenError("Inactive user")
    return user


def require_superuser(user: User = Depends(require_active_user)) -> User:
    if not user.is_superuser:
        raise ForbiddenError("Not enough permissions")
    return user