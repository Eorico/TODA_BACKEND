from fastapi import APIRouter, Depends
from backend.src.Schemas.admin_schema import CommentCreateSchema 
from Services.comment_service import  create_comment, get_comments
from Middleware.role_base_access import verify_role

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@router.post("/")
async def comment_on_event(
    data:CommentCreateSchema,
    user=Depends(verify_role("rider"))
):
    user_id = user["user_id"]
    return await create_comment(user_id, data)

@router.get("/{announcement_id}")
async def view_comments(announcement_id: str):
    return await get_comments(announcement_id)