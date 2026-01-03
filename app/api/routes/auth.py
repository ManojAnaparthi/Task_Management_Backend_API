from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, TokenResponse
from app.services.auth_service import register_user, authenticate_user, issue_tokens, refresh_tokens, logout
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

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: dict, db: Session = Depends(get_db)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    access, refresh = refresh_tokens(db, refresh_token)
    return {
        "access_token": access,
        "refresh_token": refresh
    }

@router.post("/logout", status_code=204)
def logout_user(data: dict, db: Session = Depends(get_db)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    logout(db, refresh_token)
