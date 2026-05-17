# app/Providers/AppServiceProvider.py
from app.Repositories.users.user_repository import UserRepository
from app.Repositories.users.driver_repository import DriverRepository
from app.Repositories.users.passenger_repository import PassengerRepository
from app.Repositories.admin.announcement_repository import AnnouncementRepository
from app.Repositories.admin.coding_repository import CodingRepository
from app.Repositories.admin.contribution_repository import ContributionRepository
from app.Repositories.admin.fare_repository import FareRepository
from app.Repositories.admin.lost_and_found_repository import LostFoundRepository
from app.Repositories.admin.officer_repository import OfficerRepository
from app.Repositories.admin.roster_repository import RosterRepository
from app.Repositories.admin.violation_repository import ViolationRepository

from app.Services.auth.auth_service import AuthService
from app.Services.users.driver_service import DriverService
from app.Services.users.passenger_service import PassengerService
from app.Services.admin.admin_service import AdminService
from app.Services.chat.chat_service import ChatService

from app.Http.Controllers.auth.auth_controller import AuthController
from app.Http.Controllers.users.driver_controller import DriverController
from app.Http.Controllers.users.passenger_controller import PassengerController
from app.Http.Controllers.admin.admin_controller import AdminController
from app.Http.Controllers.chat.chat_controller import ChatController

# ── Repositories ─────────────────────────────────────────────────
user_repo         = UserRepository()
driver_repo       = DriverRepository()
passenger_repo    = PassengerRepository()
announcement_repo = AnnouncementRepository()
coding_repo       = CodingRepository()
contribution_repo = ContributionRepository()
fare_repo         = FareRepository()
lost_found_repo   = LostFoundRepository()
officer_repo      = OfficerRepository()
roster_repo       = RosterRepository()
violation_repo    = ViolationRepository()

# ── Services ─────────────────────────────────────────────────────
auth_service = AuthService(user_repo, driver_repo)

driver_service = DriverService(
    driver_repo, user_repo, contribution_repo,
    violation_repo, announcement_repo, lost_found_repo,
    officer_repo, fare_repo, coding_repo,
)

passenger_service = PassengerService(
    passenger_repo, user_repo, announcement_repo,
    lost_found_repo, officer_repo, fare_repo, coding_repo,
)

admin_service = AdminService(
    driver_service,    
    driver_repo,       
    user_repo,         
    announcement_repo, 
    coding_repo,        
    contribution_repo, 
    fare_repo,         
    lost_found_repo,    
    officer_repo,    
    roster_repo,       
    violation_repo,   
)

chat_service = ChatService()

# ── Controllers ──────────────────────────────────────────────────
auth_controller      = AuthController(auth_service)
driver_controller    = DriverController(driver_service)
passenger_controller = PassengerController(passenger_service)
admin_controller     = AdminController(admin_service, auth_service)
chat_controller      = ChatController(chat_service)