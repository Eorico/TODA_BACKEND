from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_role(required_role: str):
    async def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            token = credentials.credentials

            if not token:
                raise HTTPException(status_code=401, detail="Missing token")

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=ALGORITHM
            )
            
            exp = payload.get("exp")
            if not exp or datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expired")
                
            role = payload.get("role")

            if role != required_role:
                raise HTTPException(status_code=403, detail="Access denied")

            return payload

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    return role_checker
