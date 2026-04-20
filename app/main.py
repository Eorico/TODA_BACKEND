from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routes.auth_routes import router as auth_router
from Routes.admin_routes import router as admin_router
from Routes.admin_routes import public_router as admin_router_public
from Routes.rider_routes import router as rider_router
from Routes.passenger_routes import router as passenger_router
from Routes.comment_routes import router as comment_router
from Routes.chat_routes import router as chat_router
from Config.database import init_database

app = FastAPI(
    title="TODA BACKEND",
    description="Backend API for Riders, Passengers, and Admin",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin")
app.include_router(admin_router_public, prefix="/admin", tags=["Admin"])
app.include_router(rider_router, prefix="/rider", tags=["Rider"])
app.include_router(passenger_router, prefix="/passenger", tags=["Passenger"])

app.include_router(comment_router, prefix="/comment", tags=["Comment"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.on_event("startup")
async def start_database():
    await init_database()
    print("TODA BACKEND is running on http://127.0.0.1:8000 (Press CTRL+C to quit)")
    
@app.get("/")
async def root():
    return { "message" : "Capstone Backend Running" }