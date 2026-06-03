from app.modules.health.repository import HealthRepository
from app.modules.health.service import HealthService


def get_health_repo() -> HealthRepository:
    return HealthRepository()


def get_health_service() -> HealthService:
    return HealthService(repo=get_health_repo())