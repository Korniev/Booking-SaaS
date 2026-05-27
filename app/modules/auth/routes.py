from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session, get_password_hasher
from app.core.security import PasswordHasher
from app.modules.auth.schemas import TokenResponse
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository
from app.modules.auth.dependencies import require_active_user
from app.modules.users.schemas import UserRead
from app.infra.db.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


def get_users_repo() -> UserRepository:
    return UserRepository()


def get_auth_service(
    users_repo: UserRepository = Depends(get_users_repo),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(users_repo, hasher)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_session),
    service: AuthService = Depends(get_auth_service),
):
    # OAuth2PasswordRequestForm дає: username, password
    token = await service.login(session, email=form.username, password=form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(require_active_user)):
    return user