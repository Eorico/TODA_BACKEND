from Models.comment_models import Comment
from Models.announcement_model import Announcement
from Models.user_model import User
from fastapi import HTTPException

class CommentService:

    @staticmethod
    async def create(user_id: str, data) -> dict:
        announcement = await Announcement.get(data.announcement_id)
        if not announcement:
            raise HTTPException(status_code=404, detail="Announcement not found")

        user = await User.get(user_id)
        comment = Comment(
            user=user,
            announcement=announcement,
            message=data.message
        )
        await comment.insert()
        return {"message": "Comment added"}

    @staticmethod
    async def get_by_announcement(announcement_id: str) -> list:
        return await Comment.find(
            Comment.announcement.id == announcement_id
        ).to_list()