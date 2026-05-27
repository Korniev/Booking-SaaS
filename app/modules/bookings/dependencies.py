from fastapi import Depends

from app.modules.bookings.repository import BookingRepository
from app.modules.bookings.service import BookingService
from app.modules.resources.dependencies import get_resource_service
from app.modules.resources.service import ResourceService


def get_booking_repo() -> BookingRepository:
    return BookingRepository()


def get_booking_service(
    repo: BookingRepository = Depends(get_booking_repo),
    resources: ResourceService = Depends(get_resource_service),
) -> BookingService:
    return BookingService(repo=repo, resources=resources)