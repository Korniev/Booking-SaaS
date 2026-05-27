from fastapi import Depends

from app.modules.resources.repository import ResourceRepository
from app.modules.resources.service import ResourceService


def get_resource_repo() -> ResourceRepository:
    return ResourceRepository()


def get_resource_service(repo: ResourceRepository = Depends(get_resource_repo)) -> ResourceService:
    return ResourceService(repo)