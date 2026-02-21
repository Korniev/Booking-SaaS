import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.infra.db.models.user import User
from app.modules.auth.dependencies import require_active_user, require_superuser
from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserCreate, UserRead, UserRoleUpdate, UserActiveUpdate, ChangePasswordRequest
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def register_user(
    payload: UserCreate,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
):
    return await service.register(session, payload)


@router.get("/me", response_model=UserRead)
async def read_me(user: User = Depends(require_active_user)):
    return user


@router.get("", response_model=list[UserRead])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_superuser),
):
    return await service.list_users(session, skip=skip, limit=limit)



@router.patch("/{user_id}/role", response_model=UserRead)
async def set_user_role(
    user_id: uuid.UUID,
    payload: UserRoleUpdate,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_superuser),
):
    return await service.set_role(session, user_id, payload.is_superuser)


@router.patch("/{user_id}/active", response_model=UserRead)
async def set_user_active(
    user_id: uuid.UUID,
    payload: UserActiveUpdate,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
    _: User = Depends(require_superuser),
):
    return await service.set_active(session, user_id, payload.is_active)


@router.post("/me/change-password")
async def change_my_password(
    payload: ChangePasswordRequest,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
    user: User = Depends(require_active_user),
):
    await service.change_password(session, user, payload.old_password, payload.new_password)
    return {"status": "ok"}