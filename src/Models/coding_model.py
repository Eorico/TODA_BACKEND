from beanie import Document
 
class CodingSchedule(Document):
    date: str
    day: str
    last_digit: int

    class Settings:
        name = "coding_schedule"