from fastapi import APIRouter, Depends
from Schemas.admin_schema import CommentCreateSchema
from Controllers.comment_controller import CommentController
from Middleware.role_base_access import verify_role

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@router.post("/")
async def comment_on_event(
    data: CommentCreateSchema,
    user=Depends(verify_role("driver"))
):
    return await CommentController.create(user["user_id"], data)

@router.get("/{announcement_id}")
async def view_comments(announcement_id: str):
    return await CommentController.get_by_announcement(announcement_id)