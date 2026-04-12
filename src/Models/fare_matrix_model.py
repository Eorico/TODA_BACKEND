from beanie import Document

class Fare(Document):
    
    base_fare: float
    town_proper: float
    special_trip: float
    
    class Settings:
        name = "fare_list"