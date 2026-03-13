from fastapi import APIRouter, Depends
from Middleware.role_base_access import verify_role

router = APIRouter(
        prefix="/admin",
        tags=["Admin"]
    )

@router.post("/admin-login")


@router.get("/admin")
async def admin_dashboard(user=Depends(verify_role("admin"))):
    
    return {
        "message": "Welcom Admin",
        "user_data": user
    }
    

@router.post("/announcements")
async def create_announcement(data: dict, user=Depends(verify_role("admin"))):
    announcement = ''
    
    await announcement.insert()
    
    return {"message": "Announce posted!"}

@router.get("/announcements")
async def get_announcements(user=Depends(verify_role("admin"))):
    announcements = await ""
    
    return announcements

@router.post("/officer")
async def create_officer(data: dict, user=Depends(verify_role["admin"])):
    officer = ""
    
    await officer.insert()
    
    return {"message": "Officer added"}

@router.get("/officers")
async def get_officers(user=Depends(verify_role["admin"])):
    officer = ""
    
    await officer.insert()
    
    return {"message": "Officer added"}

@router.delete("/officer/{id}")
async def delete_officer(id: str, user=Depends(verify_role("admin"))):
    officer = await ""
    
    await officer.delete()
    
    return {"message": "Officer removed"}

