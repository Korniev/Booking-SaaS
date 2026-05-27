from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

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



def create_access_token(*, subject: str, expires_minutes: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    exp_minutes = expires_minutes or settings.jwt_access_token_expire_minutes
    expire = now + timedelta(minutes=exp_minutes)

    payload: dict[str, Any] = {"sub": subject, "iat": int(now.timestamp()), "exp": int(expire.timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as e:
        raise ValueError("Invalid token") from e