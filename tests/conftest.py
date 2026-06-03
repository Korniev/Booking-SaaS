import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import db_session
from app.infra.db.models.user import User
from app.main import app
from app.modules.users.dependencies import get_user_service
from app.modules.users.service import UserService


def make_user(**kwargs):
    defaults = dict(
        id=uuid.uuid4(),
        email="test@example.com",
        full_name=None,
        hashed_password="$2b$12$hashed",
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    defaults.update(kwargs)
    user = MagicMock(spec=User)
    for k, v in defaults.items():
        setattr(user, k, v)
    return user


@pytest.fixture
def mock_user_service():
    return AsyncMock(spec=UserService)


@pytest.fixture
def client(mock_user_service):
    async def override_db_session():
        yield AsyncMock()

    def override_user_service():
        return mock_user_service

    app.dependency_overrides[db_session] = override_db_session
    app.dependency_overrides[get_user_service] = override_user_service

    with patch("app.main.init_redis", new_callable=AsyncMock), \
         patch("app.main.close_redis", new_callable=AsyncMock):
        with TestClient(app) as c:
            yield c

    app.dependency_overrides.clear()
