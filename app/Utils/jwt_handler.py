# app/Utils/JwtHandler.py
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.Exceptions.app_exception import UnauthorizedException
from dotenv import load_dotenv
import os

load_dotenv()

class JwtHandler:
    """Single Responsibility: JWT encoding/decoding only."""
    _secret    = os.getenv("SECRET_KEY", "fallback-dev-secret")
    _algorithm = "HS256"
    _ttl_hours = 24

    @classmethod
    def encode(cls, payload: dict) -> str:
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(hours=cls._ttl_hours)
        return jwt.encode(data, cls._secret, algorithm=cls._algorithm)

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(token, cls._secret, algorithms=[cls._algorithm])
        except JWTError:
            raise UnauthorizedException("Token is invalid or expired.")