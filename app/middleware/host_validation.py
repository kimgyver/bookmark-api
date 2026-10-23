from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import get_settings


class HostValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        host = request.headers.get("host", "").split(":")[0]
        if settings.debug or host in settings.allowed_hosts:
            return await call_next(request)
        raise HTTPException(status_code=400, detail="Invalid host")
