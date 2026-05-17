from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.Providers.database_provider import boot_database
from app.Http.Middleware.rate_limiter import limiter
from app.Http.Middleware.security_headers import SecurityHeadersMiddleware
from app.Exceptions.app_exception import AppException
from Routes.api import api_router
import os

app = FastAPI(
    title="TODA Sovereign",
    description="Tricycle Driver Association Management System",
    version="2.0.0",
)

# ── Exception Handlers ────────────────────────────────────────────
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# ── Rate Limiting ─────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Middleware (order matters — outermost applied last) ───────────
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files ──────────────────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ── Routes ────────────────────────────────────────────────────────
app.include_router(api_router)

# ── Lifecycle ─────────────────────────────────────────────────────
@app.on_event("startup")
async def startup() -> None:
    await boot_database()
    print("✅ MAMTTODA Backend is running.")

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": "2.0.0"}