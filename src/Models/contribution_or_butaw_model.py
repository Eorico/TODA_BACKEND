from beanie import Document
from datetime import datetime

class Contribution_Or_Butaw(Document):

    first_name: str
    last_name: str
    tricycle_body_number: str
    driver_id: str
    
    amount: float
    period_date: str
    date_paid: str
    
    payment_status: str # paid or unpaid
    notes: str

    class Settings:
        name = "contributions_or_butaw"
