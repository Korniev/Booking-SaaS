from app.infra.db.models.user import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate
from app.core.security import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, session, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(session, data.email)
        if existing:
            raise ValueError("User with this email already exists")

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        return await self.repo.create(session, user)