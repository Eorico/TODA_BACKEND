# app/Services/AuthService.py
import secrets
from app.Contracts.i_auth_service import IAuthService
from app.Repositories.users.user_repository import UserRepository
from app.Repositories.users.driver_repository import DriverRepository
from app.Utils.hasher import Hasher
from app.Utils.jwt_handler import JwtHandler
from app.Utils.file_uploader import FileUploader
from app.Exceptions.app_exception import (
    ConflictException, NotFoundException,
    UnauthorizedException, ForbiddenException, ValidationException,
)

class AuthService(IAuthService):
    """
    Single Responsibility: authentication business logic only.
    Depends on abstractions (repositories), not concretions.
    """

    def __init__(
        self,
        user_repo:   UserRepository,
        driver_repo: DriverRepository,
    ):
        self._users   = user_repo
        self._drivers = driver_repo

    async def register(self, data, extra: dict) -> dict:
        if await self._users.find_by_email(data.email):
            raise ConflictException("Email already registered.")

        is_driver = data.role == "driver"

        user = await self._users.create_user({
            "full_name":      data.full_name,
            "email":          data.email,
            "password":       Hasher.make(data.password),
            "role":           data.role,
            "contact_number": extra.get("contact_number"),
            "address":        extra.get("address"),
            "body_number":    extra.get("body_number"),
            "is_active":      not is_driver,
        })

        if is_driver:
            license_path = await FileUploader.upload(
                extra.get("license_url"), str(user.id)
            )
            orcr_path = await FileUploader.upload(
                extra.get("orcr_url"), str(user.id)
            )
            parts  = data.full_name.split(" ", 1)
            f_name = parts[0]
            l_name = parts[1] if len(parts) > 1 else ""

            await self._drivers.create_profile({
                "full_name":               f_name,
                "last_name":               l_name,
                "body_number":             extra.get("body_number") or "---",
                "contact":                 extra.get("contact_number") or "-",
                "email":                   data.email,
                "address":                 extra.get("address") or "Not Specified",
                "license_url":             license_path,
                "orcr_url":                orcr_path,
                "expiration_date_license": extra.get("expiration_date_license"),
                "expiration_date_orcr":    extra.get("expiration_date_orcr"),
                "status":                  "Inactive",
                "member_status":           "pending",
            })

        return {"message": "Registered successfully. Drivers pending approval."}

    async def login(self, data) -> dict:
        user = await self._users.find_by_email(data.email)
        if not user:
            raise NotFoundException("User")
        if not Hasher.check(data.password, user.password):
            raise UnauthorizedException("Invalid password.")

        if data.role and user.role != data.role:
            raise ForbiddenException(
                f"Account is registered as a {user.role}."
            )

        if user.role == "driver":
            body = getattr(data, "body_number", None)
            if not body or not body.strip():
                raise ValidationException("Body number is required.")
            if user.body_number != body.strip():
                raise UnauthorizedException("Body number is incorrect.")

            if not user.is_active:
                profile = await self._drivers.find_by_email(user.email)
                return {
                    "role":   user.role,
                    "status": profile.member_status if profile else "pending",
                }

        token = JwtHandler.encode({
            "user_id": str(user.id),
            "role":    user.role,
            "email":   user.email,
        })
        return {"access_token": token, "role": user.role, "status": "approved"}

    async def forgot_password(self, data) -> dict:
        user = await self._users.find_by_email(data.email)
        if not user:
            raise NotFoundException("Email")
        token = secrets.token_hex(32)
        await self._users.set_reset_token(data.email, token)
        return {"message": "Reset token generated.", "reset_token": token}

    async def verify_code(self, data) -> dict:
        user = await self._users.find_by_email(data.email)
        if not user or user.reset_token != data.code:
            raise ValidationException("Invalid or expired code.")
        return {"message": "Code verified."}

    async def reset_password(self, data) -> dict:
        user = await self._users.find_by_email(data.email)
        if not user or user.reset_token != data.code:
            raise ValidationException("Invalid session.")
        user.password    = Hasher.make(data.new_password)
        user.reset_token = None
        await user.save()
        return {"message": "Password reset successfully."}