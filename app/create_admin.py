import asyncio
from Models.user_model import User
from Utils.password import hash_password
from Config.database import init_database

async def create_admin():
    await init_database()
    
    existing = await User.find_one(User.email == "admin@gmail.com")
    
    if existing:
        print("Admin already exist")
        return
    
    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password=hash_password("admin123"),
        role="admin"
    )
    
    await admin.insert()
    
    print("Admin created successfully")
    
if __name__ == "__main__":
    asyncio.run(create_admin())