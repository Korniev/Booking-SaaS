from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import PasswordHasher, create_access_token
from app.modules.users.repository import UserRepository


class AuthService:
    def __init__(self, users_repo: UserRepository, hasher: PasswordHasher):
        self.users_repo = users_repo
        self.hasher = hasher

    async def login(self, session: AsyncSession, email: str, password: str) -> str:
        user = await self.users_repo.get_by_email(session, email)
        if not user:
            raise UnauthorizedError("Invalid credentials")

        if not user.is_active:
            raise ForbiddenError("User is inactive")

        if not self.hasher.verify(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")

        return create_access_token(subject=str(user.id))