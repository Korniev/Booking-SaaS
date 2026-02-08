from fastapi import FastAPI

from app.core.logging import configure_logging
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as users_router

configure_logging()

app = FastAPI(title="Booking SaaS", version="0.1.0")
app.include_router(health_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"name": "booking-saas", "version": "0.1.0"}