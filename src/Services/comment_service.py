from Models.comment_model import Comment
from Models.announcement_model import Announcement
from Models.user_model import User
from fastapi import HTTPException

async def create_comment(user_id: str, data):
    announcement = await Announcement.get(data.announcement_id)

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    user = await User.get(user_id)

    comment = Comment(
        user=user, 
        announcement=announcement,
        message=date.message
    )

    await comment.insert(
        return {"message": "Comment added"}
    )

async def get_comments(announcement_id: str):
    comments = await Comment.find(
        Comment.announcement.id == announcement_id
    ).to_list()

        return comments
    comment.announcement.id 