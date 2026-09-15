from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles

from src.admin import setup_admin

from src.api.errors import http_exception_handler
from src.api.errors import service_error_handler
from src.api.v1.router import router as api_v1_router
from src.services.exceptions import ServiceError

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

app = FastAPI(title="Biomirix Lucky Wheel")

app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

app.include_router(
    api_v1_router,
    prefix="/api/v1"
)

setup_admin(app)
