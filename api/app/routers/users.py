from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.users import get_user_repository, UserRepository
from app.schemas.users import UserRead, UserCreate
from app.services.users import UserService
from app.services.auth import AuthService
from app.services.auth import get_auth_service
from app.schemas.users import VerifyEmailToken

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_user_service(repo: UserRepository = Depends(get_user_repository),
                           auth: AuthService = Depends(get_auth_service)) -> UserService:
    return UserService(repo, auth)

async def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)


@user_router.post("/", response_model=UserRead)
async def create(user: UserCreate ,
        service: UserService = Depends(get_user_service)):
    new_user = await service.create(user)
    return new_user



@user_router.post("/verify-email", response_model=UserRead)
async def verify_email(
    token: VerifyEmailToken,
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service)
):
    email = await auth_service.verify_email_token(token.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verify email token")
    user = await user_service.get_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email is already verified"
        )

    return await user_service.update(user.id, {"is_active": True})


