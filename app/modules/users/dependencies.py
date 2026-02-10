from fastapi import Depends

from app.core.dependencies import get_password_hasher
from app.core.security import PasswordHasher
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_user_repo() -> UserRepository:
    return UserRepository()


def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserService:
    return UserService(repo=repo, hasher=hasher)