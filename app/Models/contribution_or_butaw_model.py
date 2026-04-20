from beanie import Document
from typing import Optional

class Contribution_Or_Butaw(Document):

    fname: str
    lname: str
    body: str
    driverid: str
    amount: float
    period: str
    date: str
    status: str  # paid, partial, or unpaid
    notes: Optional[str] = None

    class Settings:
        name = "contributions_or_butaw"
