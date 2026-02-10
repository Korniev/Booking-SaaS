from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import PasswordHasher
from app.infra.db.models.user import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate


class UserService:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def register(self, session: AsyncSession, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(session, data.email)
        if existing:
            raise ValueError("User with this email already exists")

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=self.hasher.hash(data.password),
        )
        return await self.repo.create(session, user)