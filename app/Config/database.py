from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.Models.user_model import User
from app.Models.announcement_model import Announcement
from app.Models.chat_model import Chatroom
from app.Models.coding_model import CodingSchedule
from app.Models.comment_models import Comment
from app.Models.contribution_or_butaw_model import Contribution_Or_Butaw
from app.Models.fare_matrix_model import Fare
from app.Models.lostfound_model import LostFound
from app.Models.message_model import Message
from app.Models.officer_model import Officer
from app.Models.driver_profile_model import RiderProfile
from app.Models.roster_model import MemberRoster
from app.Models.violation_model import Violation
from dotenv import load_dotenv
import os

load_dotenv()

async def init_database():
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    
    database = client[os.getenv("DATABASE_NAME")]
    
    await init_beanie(
        database=database,
        document_models=[
            User,
            Announcement,
            Chatroom,
            CodingSchedule,
            Comment,
            Contribution_Or_Butaw,
            Fare,
            LostFound,
            Message,
            Officer,
            RiderProfile,
            MemberRoster,
            Violation
        ]
    )