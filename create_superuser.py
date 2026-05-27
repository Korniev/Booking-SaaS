import asyncio

from app.core.dependencies import get_password_hasher
from app.infra.db.session import AsyncSessionFactory
from app.infra.db.models.user import User


async def create_superuser():
    async with AsyncSessionFactory() as session:
        hasher = get_password_hasher()

        user = User(
            email="admin@example.com",
            full_name="Admin",
            hashed_password=hasher.hash("admin123"),
            is_active=True,
            is_superuser=True,
        )

        session.add(user)
        await session.commit()
        print("Superuser created!")


if __name__ == "__main__":
    asyncio.run(create_superuser())