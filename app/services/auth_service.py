from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    ALGORITHM
)

def register_user(db: Session, email: str, password: str):
    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def issue_tokens(db: Session, user: User):
    access = create_access_token(str(user.id))
    
    # Create token with unique ID
    token_id = str(uuid.uuid4())
    refresh = create_refresh_token(str(user.id), token_id)

    token = RefreshToken(
        id=uuid.UUID(token_id),
        user_id=user.id,
        token_hash=hash_password(refresh),
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(token)
    db.commit()

    return access, refresh

def refresh_tokens(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_id = payload.get("jti")
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        if not token_id:
            raise HTTPException(status_code=401, detail="Invalid token format")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Find the token by ID
    matched_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.id == token_id,
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False
        )
        .first()
    )

    if not matched_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or reused"
        )

    # Check if token is expired
    if matched_token.expires_at < datetime.utcnow():
        matched_token.revoked = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    # ROTATION: revoke old token
    matched_token.revoked = True
    db.commit()

    # Issue new tokens
    new_token_id = str(uuid.uuid4())
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id, new_token_id)

    new_token = RefreshToken(
        id=uuid.UUID(new_token_id),
        user_id=user_id,
        token_hash=hash_password(new_refresh),
        expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(new_token)
    db.commit()

    return new_access, new_refresh

def logout(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_id = payload.get("jti")
        
        if not token_id:
            raise HTTPException(status_code=401, detail="Invalid token format")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token = db.query(RefreshToken).filter(
        RefreshToken.id == token_id,
        RefreshToken.revoked == False
    ).first()

    if token:
        token.revoked = True
        db.commit()
    else:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
