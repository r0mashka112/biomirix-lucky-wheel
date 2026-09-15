from fastapi import APIRouter

from src.api.v1.endpoints import me
from src.api.v1.endpoints import spins
from src.api.v1.endpoints import health
from src.api.v1.endpoints import settings

router = APIRouter()

router.include_router(
    health.router,
    tags=["health"]
)

router.include_router(
    me.router,
    prefix="/me",
    tags=["me"]
)

router.include_router(
    spins.router,
    prefix="/spins",
    tags=["spins"]
)

router.include_router(
    settings.router,
    prefix="/settings",
    tags=["settings"]
)
