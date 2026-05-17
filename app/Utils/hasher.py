# app/Utils/Hasher.py
from passlib.context import CryptContext

class Hasher:
    """Single Responsibility: password hashing only."""
    _ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def make(cls, plain: str) -> str:
        return cls._ctx.hash(plain)

    @classmethod
    def check(cls, plain: str, hashed: str) -> bool:
        return cls._ctx.verify(plain, hashed)