from fastapi import APIRouter, Depends, Body, HTTPException
from Middleware.role_base_access import verify_role
from Models.announcement_model import Announcement
from Models.officer_model import Officer
from Schemas.user_schema import LoginSchema
from Services.auth_service import login

# routes of admin
router = APIRouter(
        prefix="/admin",
        tags=["Admin"],
        dependencies=[Depends(verify_role("admin"))]
    )

# admin dashboard
@router.get("/admin-dashboard")
async def admin_dashboard(user=Depends(verify_role("admin"))):
    
    return {
        "message": "Welcome Admin",
        "user_data": user
    }

# admin login
@router.post("/admin-login")
async def admin_login(data: LoginSchema = Body(...)):
    
    result = await login(data)
    
    if result["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied: not admin")
    
    return {
        "message": "Admin logged in successfully",
        "access_token": result["access_token"]
    }
    
# admin create announcement
@router.post("/announcements")
async def create_announcement(data: dict, user=Depends(verify_role("admin"))):
    announcement = Announcement(**data)
    
    await announcement.insert()
    
    return {"message": "Announce posted!"}

# admin get announcements
@router.get("/announcements")
async def get_announcements(user=Depends(verify_role("admin"))):
    announcements = await Announcement.find_all().to_list()
    
    return announcements

#admin create officer
@router.post("/officer")
async def create_officer(data: dict, user=Depends(verify_role["admin"])):
    officer = Officer(**data)
    
    await officer.insert()
    
    return {"message": "Officer added"}

# admin get officer
@router.get("/officers")
async def get_officers(user=Depends(verify_role["admin"])):
    officer = await Officer.find_all().to_list()
    
    await officer.insert()
    
    return {"message": "Officer added"}

# delete admin officer
@router.delete("/officer/{id}")
async def delete_officer(id: str, user=Depends(verify_role("admin"))):
    officer = await Officer.get(id)
    
    await officer.delete()
    
    return {"message": "Officer removed"}

