from fastapi import FastAPI
from Routes.auth_routes import router as auth_router
from Routes.admin_routes import router as admin_router
from Config.database import init_database

app = FastAPI(
    title="TODA BACKEND",
    description="Backend API for Riders, Passengers, and Admin",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
async def start_database():
    await init_database()
    
@app.get("/")
async def root():
    return { "message" : "Capstone Backend Running" }