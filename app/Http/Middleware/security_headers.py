# app/Http/Middleware/security_headers.py
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.datastructures import MutableHeaders

class SecurityHeadersMiddleware:
    """Pure ASGI middleware — zero buffering overhead."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Content-Type-Options"] = "nosniff"
                headers["X-Frame-Options"]        = "DENY"
                headers["X-XSS-Protection"]       = "1; mode=block"
            await send(message)

        await self.app(scope, receive, send_with_headers)