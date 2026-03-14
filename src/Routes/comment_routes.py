from fastapi import  APIRouter, Depends
from Schemas.comment_schema import CommentCreateSchema 
from Services.comment_service import  create_comment, get_comments
from Middleware.role_base_access import verify_one

route = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@route.post("/")
async def comment_on_event(
    data:CommentCreateSchema,
    user=Depends(verify_one("rider"))
):

    user_id = user["user_id"]
    return await create_comment(user_id, data)

@route.get("/{announcement_id}")
async def view_comments(announcement_id: str):
    return await get_comments(announcement_id)