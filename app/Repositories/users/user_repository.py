# app/Repositories/users/user_repository.py
from app.Repositories.base_repository import BaseRepository
from app.Models.users.user_model import User

class UserRepository(BaseRepository):
    model = User

    async def find_by_email(self, email: str) -> User | None:
        return await User.find_one(User.email == email, fetch_links=False)

    async def create_user(self, data: dict) -> User:
        return await self.create(data)

    async def activate(self, email: str) -> None:
        # find() returns a FindMany query object — update() works on it directly
        await User.find(User.email == email).update(
            {"$set": {"is_active": True}}
        )

    async def delete_by_email(self, email: str) -> None:
        user = await self.find_by_email(email)
        if user:
            await user.delete()

    async def set_reset_token(self, email: str, token: str | None) -> None:
        await User.find(User.email == email).update(
            {"$set": {"reset_token": token}}
        )

    async def clear_reset_token(self, email: str) -> None:
        await self.set_reset_token(email, None)