from fastapi import FastAPI

from app.core.config import settings
from app.core.error_handlers import setup_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware.request_logging import RequestLoggingMiddleware
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as users_router
from app.modules.auth.routes import router as auth_router

configure_logging(level=settings.log_level)

app = FastAPI(title="Booking SaaS", version="0.1.0")

setup_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"name": "booking-saas", "version": "0.1.0"}