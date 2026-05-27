import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.models.user import User


class UserRepository:

    async def get_by_id(self, session: AsyncSession, user_id: uuid.UUID) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list_users(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[User]:
        result = await session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def set_superuser(self, session: AsyncSession, user_id: uuid.UUID, is_superuser: bool) -> User | None:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_superuser=is_superuser)
        )
        await session.commit()
        return await self.get_by_id(session, user_id)

    async def set_active(self, session: AsyncSession, user_id: uuid.UUID, is_active: bool) -> User | None:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=is_active)
        )
        await session.commit()
        return await self.get_by_id(session, user_id)

    async def set_password_hash(self, session: AsyncSession, user_id: uuid.UUID, hashed_password: str) -> None:
        await session.execute(
            update(User).where(User.id == user_id).values(hashed_password=hashed_password)
        )
        await session.commit()