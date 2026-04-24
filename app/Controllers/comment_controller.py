from Services.comment_service import CommentService

class CommentController:

    @staticmethod
    async def create(user_id: str, data) -> dict:
        return await CommentService.create(user_id, data)

    @staticmethod
    async def get_by_announcement(announcement_id: str) -> list:
        return await CommentService.get_by_announcement(announcement_id)