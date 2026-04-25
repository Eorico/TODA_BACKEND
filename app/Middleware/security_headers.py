from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        res = await call_next(request)
        res.headers["X-Content-Type-Options"] = "nosniff"
        res.headers["X-Frame-Options"] = "DENY"
        res.headers["X-XSS-Protection"] = "1; mode=block"
        res.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        res.headers["Cache-Control"] = "no-store"

        # ✅ Only apply HSTS in production (HTTPS), never on localhost
        host = request.headers.get("host", "")
        is_local = host.startswith("127.0.0.1") or host.startswith("localhost")
        is_https = request.url.scheme == "https"

        if is_https and not is_local:
            res.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return res