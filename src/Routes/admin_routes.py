from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role

router = APIRouter()

@router.post("/admin-login")


@router.get("/admin")
async def admin_dashboard(user=Depends(verify_role("admin"))):
    
    return {
        "message": "Welcom Admin",
        "user_data": user
    }