from Routes.auth_driver_routes import router as auth_driver_router
from Routes.auth_passenger_routes import router as auth_passenger_router
from Routes.auth_shared_routes import router as auth_shared_routes
from Routes.admin_routes import router as admin_router
from Routes.admin_routes import public_router as admin_router_public
from Routes.driver_routes import router as rider_router
from Routes.passenger_routes import router as passenger_router
from Routes.comment_routes import router as comment_router
from Routes.chat_routes import router as chat_router
from Config.database import init_database
from Middleware.rate_limiter import limiter
from Middleware.security_headers import SecurityHeadersMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import os

app = FastAPI(
    title="TODA BACKEND",
    description="Backend API for Riders, Passengers, and Admin",
    version="1.0.0"
)

#   Rate limiting  
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#  Trust Render's proxy so real client IPs work with slowapi  
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Security headers 
app.add_middleware(SecurityHeadersMiddleware)

#  CORS — update to your actual frontend URL 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Static files 
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

#  Routers 
app.include_router(auth_driver_router, prefix="/auth")
app.include_router(auth_passenger_router, prefix="/auth")
app.include_router(auth_shared_routes, prefix="/auth")

app.include_router(admin_router, prefix="/admin")
app.include_router(admin_router_public, prefix="/admin")

app.include_router(rider_router, prefix="/rider")
app.include_router(passenger_router, prefix="/passenger")

app.include_router(comment_router, prefix="/comment")
app.include_router(chat_router, prefix="/chat")

@app.on_event("startup")
async def start_database():
    await init_database()
    print("TODA BACKEND is running!")

@app.get("/")
async def root():
    return {"message": "Capstone Backend Running"}