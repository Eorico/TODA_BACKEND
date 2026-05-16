from app.Models.user_model import User
from app.Models.driver_profile_model import RiderProfile
from app.Models.passenger_profile_model import PassengerProfile  # ← ADD THIS IMPORT
from app.Utils.password import hash_password, verify_password
from app.Utils.jwt_handler import create_token
from app.Utils.upload_license_img import handle_file_upload
from fastapi import HTTPException 
import secrets 

class AuthService:

    @staticmethod
    async def signup(data, extra_data: dict) -> dict:
        if await User.find_one(User.email == data.email):
            raise HTTPException(400, "Email already registered")

        is_driver = data.role == "driver"
        user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            contact_number=extra_data.get("contact_number"),
            is_active=not is_driver,
            body_number=extra_data.get("body_number"),
        )
        await user.insert()

        if is_driver:
            license_file = extra_data.get("license_url")  
            orcr_file = extra_data.get("orcr_url")

            license_path = None
            if license_file:
                license_path = await handle_file_upload(license_file, str(user.id))
                
            orcr_path = None
            if orcr_file:
                orcr_path = await handle_file_upload(orcr_file, str(user.id))

            name_parts = data.full_name.split(" ", 1)
            f_name = name_parts[0]
            l_name = name_parts[1] if len(name_parts) > 1 else ""

            profile = RiderProfile(
                full_name=f_name,
                last_name=l_name,
                body_number=extra_data.get("body_number") or "---",
                contact=extra_data.get("contact_number") or "-",
                email=data.email,
                license_url=license_path,
                orcr_url=orcr_path,
                expiration_date_license=extra_data.get("expiration_date_license"), 
                expiration_date_orcr=extra_data.get("expiration_date_orcr"),       
                address=extra_data.get("address") or "Not Specified",
                status="Inactive",
                member_status="pending",
                user=user
            )
            try:
                await profile.insert()
            except Exception as e:
                raise HTTPException(500, f"Profile creation failed: {str(e)}")

        else:
            # ── CREATE PASSENGER PROFILE ── ← ADD THIS ENTIRE BLOCK
            passenger_profile = PassengerProfile(
                full_name=data.full_name,
                email=data.email,
                contact=extra_data.get("contact_number"),
                address=extra_data.get("address") or "Not Specified",
            )
            try:
                await passenger_profile.insert()
            except Exception as e:
                raise HTTPException(500, f"Passenger profile creation failed: {str(e)}")

        return {"message": "Registration successful. Drivers pending admin approval."}