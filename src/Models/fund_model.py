from beanie import Document, View
from datetime import datetime

class Fund(Document):

    rider_id: str
    amount: float
    description: str
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "fund_records"
