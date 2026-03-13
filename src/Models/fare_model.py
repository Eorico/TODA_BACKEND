from beanie import Document
from datetime import datetime

class Fare(Document):
    route: str
    price: float 
    updated_at: datetime = datetime.utcnow()
    
    class Settings: 
        name = "fare_list"