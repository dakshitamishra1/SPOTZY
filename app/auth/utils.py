from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
import re

SECRET_KEY = "MYSECRETJWTKEY"  # CHANGE THIS IN PRODUCTION
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------
# PASSWORD VALIDATION
# -------------------------------

def validate_password(password: str):
    """
    Validates password strength:
    - Minimum 8 chars
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 digit
    - At least 1 special character
    - Maximum 72 chars (bcrypt limit)
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot exceed 72 characters (bcrypt limit)")

    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")

    if not re.search(r"[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character")

    return True


# -------------------------------
# PASSWORD HASHING
# -------------------------------

def hash_password(password: str):
    password = password[:72]   # enforce bcrypt limit
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# JWT TOKEN CREATION
# -------------------------------

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
