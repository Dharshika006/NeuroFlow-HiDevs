import uuid

from starlette.middleware.base import (
    BaseHTTPMiddleware
)


class SecurityHeadersMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        response = await call_next(
            request
        )

        response.headers[
            "X-Content-Type-Options"
        ] = "nosniff"

        response.headers[
            "X-Frame-Options"
        ] = "DENY"

        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000"

        response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "img-src 'self' data: https://fastapi.tiangolo.com; "
    "font-src 'self' https://cdn.jsdelivr.net"
    "connect-src 'self' https://cdn.jsdelivr.net"
)   

        response.headers[
            "X-Request-ID"
        ] = str(uuid.uuid4())

        return response