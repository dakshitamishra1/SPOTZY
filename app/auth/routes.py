from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.auth.utils import validate_password

from app.database import Base, engine, SessionLocal
from app.auth.models import User
from app.auth.schema import UserSignup, UserLogin, UserResponse, Token
from app.auth.utils import (
    hash_password, 
    verify_password, 
    create_access_token,
    SECRET_KEY, 
    ALGORITHM
)

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SIGNUP
@router.post("/signup", response_model=UserResponse)
def signup(user: UserSignup, db: Session = Depends(get_db)):

    # 🔥 FIRST validate password format
    validate_password(user.password)

    # 🔥 Check if user already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")

    # 🔥 Hash password
    hashed = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# LOGIN — returns JWT token
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(400, "Invalid email or password")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}


# GET CURRENT USER (Protected Route)
@router.get("/me", response_model=UserResponse)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except:
        raise HTTPException(401, "Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "User not found")

    return user
