from beanie import Document

class Officer(Document):

    name: str
    position: str
    contact: str

    class Settings:
        name = "officers"