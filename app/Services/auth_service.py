from Models.user_model import User
from Models.riderprofile_model import RiderProfile
from Utils.password import hash_password, verify_password
from Utils.jwt_handler import create_token
from Utils.upload_license_img import handle_file_upload
from fastapi import HTTPException 
import secrets 

class AuthService:

    @staticmethod
    async def signup(data, extra_data: dict) -> dict:
        # 1. Duplicate Check
        if await User.find_one(User.email == data.email):
            raise HTTPException(400, "Email already registered")

        # 2. Create Login User (Inactive by default for drivers)
        is_driver = data.role == "driver"
        user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            contact_number=extra_data.get("contact_number"),
            is_active=not is_driver
        )
        await user.insert()

        if is_driver:
            license_file = extra_data.get("license_url")  
            print(f"📎 license_file: {license_file}")       

            license_path = None
            if license_file:
                license_path = await handle_file_upload(license_file, str(user.id))
                print(f"✅ license_path length: {len(license_path) if license_path else 0}")

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
                address=extra_data.get("address") or "Not Specified",
                status="Inactive",
                member_status="pending",
                user=user
            )
            try:
                await profile.insert()
                print(f"✅ RiderProfile created: {profile.id}")
            except Exception as e:
                print(f"❌ RiderProfile insert failed: {e}")
                raise HTTPException(500, f"Profile creation failed: {str(e)}")

        return {"message": "Registration successful. Drivers pending admin approval."}

    @staticmethod
    async def login(data) -> dict:
        user = await User.find_one(User.email == data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        if user.role == "driver":
            if not user.is_active:    
                profile = await RiderProfile.find_one(RiderProfile.email == user.email)
                status = profile.member_status if profile else "pending"
                return {
                    "access_token": None,
                    "role": user.role,
                    "status": status  
                }

        token = create_token({"user_id": str(user.id), "role": user.role})
        return {
            "access_token": token,
            "role": user.role,
            "status": "approved"   
        }

    @staticmethod
    async def forgot_password(data) -> dict:
        user = await User.find_one(User.email == data.email)
        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        token = secrets.token_hex(16)
        user.reset_token = token
        await user.save()
        return {"message": "Password reset token generated", "reset_token": token}
    
    @staticmethod
    async def verify_code(data) -> dict:
        user = await User.find_one(User.email == data.email)
        if not user or user.reset_token != data.code:
            raise HTTPException(status_code=400, detail="Invalid or Expired code")
        
        return {"message": "Code verified successfully"}
    
    @staticmethod
    async def reset_password(data) -> dict:
        user = await User.find_one(User.email == data.email)
        if not user or user.reset_token != data.code:
            raise HTTPException(status_code=400, detail="Invalid Session")
        
        user.password = hash_password(data.new_password)
        user.reset_token = None
        await user.save()
        return {"message": "Password reset successfully"}