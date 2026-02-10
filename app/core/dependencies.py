from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordHasher, PasslibBcryptHasher
from app.infra.db.session import get_session


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return PasslibBcryptHasher()