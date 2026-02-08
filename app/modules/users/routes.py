from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import db_session
from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def register_user(
    payload: UserCreate,
    session: AsyncSession = Depends(db_session),
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.register(session, payload)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))