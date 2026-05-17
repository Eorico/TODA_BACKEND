# app/Providers/DatabaseProvider.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.Models.users.user_model import User
from app.Models.users.driver_profile_model import DriverProfile
from app.Models.users.passenger_profile_model import PassengerProfile
from app.Models.admin.announcement_model import Announcement
from app.Models.admin.coding_model import CodingSchedule
from app.Models.admin.contribution_or_butaw_model import Contribution_Or_Butaw as Contribution
from app.Models.admin.fare_matrix_model import Fare
from app.Models.admin.lostfound_model import LostFound
from app.Models.admin.roster_model import MemberRoster
from app.Models.admin.officer_model import Officer
from app.Models.admin.violation_model import Violation
from app.Models.chat.chat_model import Chatroom
from app.Models.chat.message_model import Message
from dotenv import load_dotenv
import os

load_dotenv()

async def boot_database() -> None:
    client   = AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    database = client[os.getenv("DATABASE_NAME")]
    await init_beanie(
        database=database,
        document_models=[
            User, DriverProfile, PassengerProfile,
            Announcement, CodingSchedule, Contribution,
            Fare, LostFound, MemberRoster, Officer,
            Violation, Chatroom, Message,
        ],
    )