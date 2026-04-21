from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from Models.user_model import User
from Models.announcement_model import Announcement
from Models.chat_model import Chatroom
from Models.coding_model import CodingSchedule
from Models.comment_models import Comment
from Models.contribution_or_butaw_model import Contribution_Or_Butaw
from Models.fare_matrix_model import Fare
from Models.lostfound_model import LostFound
from Models.message_model import Message
from Models.officer_model import Officer
from Models.riderprofile_model import RiderProfile
from Models.roster_model import MemberRoster
from Models.violation_model import Violation
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