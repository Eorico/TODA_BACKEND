 from beanie import Document
 
 class CodingSchedule(Document):
    plate_last_digit: int
    day: str

    class Settings:
        name = "Coding_schedule"