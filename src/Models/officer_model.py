from beanie import Document

class Officer(Document):

    first_name: str
    middle_name: str
    last_name: str
    
    officer_id: str
    role: str
    duty_status: str
    
    phone: str
    email: str

    class Settings:
        name = "officers"