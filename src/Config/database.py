from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.Models.user_model import User
from dotenv import load_dotenv
import os

load_dotenv()

async def init_database():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    
    database = client[os.getenv("DATABASE_NAME")]
    
    await init_beanie(
        database=database,
        document_models=[User]
    )