from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth import AuthService, get_auth_service
from app.schemas.enum import TokenType
from app.services.users import UserService, get_user_service
from app.utils.exceptions import CredentialsException, TokenExpiredException
from app.auth.tokens import generate_jwt_token
from app.models import User
from app.auth.deps import get_current_user
from app.schemas.users import AccessTokenResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login",response_model=AccessTokenResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
      ):
    current_user = await user_service.get_by_email(email=form_data.username)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    access_token, refresh_token = await auth_service.authenticate(form_data.password, current_user)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24 * 2
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(request: Request, service: AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        user = await service.get_user_by_token(refresh_token, TokenType.REFRESH)
    except TokenExpiredException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except CredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    new_access_token = generate_jwt_token({"sub": user.email}, TokenType.ACCESS)
    return {"access_token": new_access_token, "token_type": "bearer"}


@auth_router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user