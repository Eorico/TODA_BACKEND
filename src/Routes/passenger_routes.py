from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role

router = APIRouter()

@router.get("/passenger-dashboard")
async def passenger_dashboard(user=Depends(verify_role("passenger"))):
    return {"message": "Welcome Passenger"}