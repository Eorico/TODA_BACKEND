# Routes/api.py
from fastapi import APIRouter
from Routes.auth.auth      import router as auth_router
from Routes.admin.admin_routes     import router as admin_router, public_router as admin_public_router
from Routes.users.driver_routes    import router as driver_router
from Routes.users.passenger_routes import router as passenger_router, public_router as passenger_public_router
from Routes.chat.chat_routes      import router as chat_router

api_router = APIRouter()

api_router.include_router(auth_router,             prefix="/auth")
api_router.include_router(admin_public_router,     prefix="/admin")
api_router.include_router(admin_router,            prefix="/admin")
api_router.include_router(driver_router,           prefix="/driver")
api_router.include_router(passenger_public_router, prefix="/passenger")
api_router.include_router(passenger_router,        prefix="/passenger")
api_router.include_router(chat_router,             prefix="/chat")