from fastapi import FastAPI
from Routes.auth_routes import router as auth_router
from Routes.admin_routes import router as admin_router
from Routes.rider_routes import router as rider_router
from Routes.passenger_routes import router as passenger_router
from Config.database import init_database

app = FastAPI(
    title="TODA BACKEND",
    description="Backend API for Riders, Passengers, and Admin",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(rider_router, prefix="/rider", tags=["Rider"])
app.include_router(passenger_router, prefix="/passenger", tags=["Passenger"])

@app.on_event("startup")
async def start_database():
    await init_database()
    print("TODA BACKEND is running on http://127.0.0.1:8000 (Press CTRL+C to quit)")
    
@app.get("/")
async def root():
    return { "message" : "Capstone Backend Running" }