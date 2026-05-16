from beanie import Document
from typing import Optional

class Contribution_Or_Butaw(Document):

    full_name: str
    last_name: str
    body_number: str
    driverid: str
    amount: float
    date: str
    status: str  # paid, partial, or unpaid
    notes: Optional[str] = None

    class Settings:
        name = "contributions_or_butaw"
