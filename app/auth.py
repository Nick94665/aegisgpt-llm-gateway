from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import settings
from typing import Optional

security = HTTPBearer()

def create_jwt(payload: dict, secret: Optional[str] = None):
    secret = secret or settings.JWT_SECRET
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def decode_jwt(token: str, secret: Optional[str] = None):
    secret = secret or settings.JWT_SECRET
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
        return data
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    data = decode_jwt(token)
    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # token expected to have "sub" and "roles"
    return data
