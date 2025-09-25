from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..auth import verify_password, create_access_token
from ..models import Token, UserRole
from ..config import get_settings

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    role = None
    username = None

    if verify_password(form_data.password, UserRole.ADMIN):
        role = UserRole.ADMIN
        username = "admin"
    elif verify_password(form_data.password, UserRole.USER):
        role = UserRole.USER
        username = "user"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"username": username, "role": role},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")