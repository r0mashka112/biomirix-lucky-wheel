from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.services.exceptions import ServiceError


async def service_error_handler(
    _request: Request,
    exc: ServiceError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"reason": exc.reason},
    )


async def http_exception_handler(
    _request: Request,
    exc: HTTPException,
) -> JSONResponse:
    if isinstance(exc.detail, dict) and "reason" in exc.detail:
        content = exc.detail
    else:
        content = {"reason": str(exc.detail)}

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )
