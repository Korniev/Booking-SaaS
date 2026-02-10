from __future__ import annotations

from dataclasses import dataclass
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed_password: str) -> bool: ...


@dataclass(frozen=True)
class PasslibBcryptHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
