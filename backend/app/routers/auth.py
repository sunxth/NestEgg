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
    username = form_data.username.lower() if form_data.username else "user"

    # Map username to expected role and validate password
    if username in ["husband", "admin"]:
        # Husband/Admin login
        if verify_password(form_data.password, UserRole.ADMIN):
            role = UserRole.ADMIN
            username = "admin"
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="管理员密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif username in ["wife", "user"]:
        # Wife/User login
        if verify_password(form_data.password, UserRole.USER):
            role = UserRole.USER
            username = "user"
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # Fallback: try both passwords
        if verify_password(form_data.password, UserRole.ADMIN):
            role = UserRole.ADMIN
            username = "admin"
        elif verify_password(form_data.password, UserRole.USER):
            role = UserRole.USER
            username = "user"
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"username": username, "role": role},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")