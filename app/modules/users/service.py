import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, BadRequestError
from app.core.security import PasswordHasher
from app.infra.db.models.user import User
from app.modules.users.exceptions import UserAlreadyExistsError
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def register(self, session: AsyncSession, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(session, data.email)
        if existing:
            raise UserAlreadyExistsError("User with this email already exists")

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=self.hasher.hash(data.password),
        )
        return await self.repo.create(session, user)

    async def list_users(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repo.list_users(session, skip=skip, limit=limit)

    async def set_role(self, session: AsyncSession, user_id: uuid.UUID, is_superuser: bool) -> User:
        user = await self.repo.set_superuser(session, user_id, is_superuser)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def set_active(self, session: AsyncSession, user_id: uuid.UUID, is_active: bool) -> User:
        user = await self.repo.set_active(session, user_id, is_active)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def change_password(self, session: AsyncSession, user: User, old_password: str, new_password: str) -> None:
        if not self.hasher.verify(old_password, user.hashed_password):
            raise BadRequestError("Old password is incorrect")
        new_hash = self.hasher.hash(new_password)
        await self.repo.set_password_hash(session, user.id, new_hash)