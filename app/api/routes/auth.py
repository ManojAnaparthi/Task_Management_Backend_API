from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, TokenResponse
from app.services.auth_service import register_user, authenticate_user, issue_tokens
from app.db.session import SessionLocal

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password)
    access, refresh = issue_tokens(db, user)
    return {
        "access_token": access,
        "refresh_token": refresh
    }

@router.post("/login", response_model=TokenResponse)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access, refresh = issue_tokens(db, user)
    return {
        "access_token": access,
        "refresh_token": refresh
    }
