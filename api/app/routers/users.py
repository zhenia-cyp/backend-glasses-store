from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.users import get_user_repository, UserRepository
from app.schemas.users import UserRead, UserCreate
from app.services.users import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)


@user_router.post("/", response_model=UserRead)
async def create(user: UserCreate ,
        service: UserService = Depends(get_user_service)):
    existing_user = await service.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    new_user = await service.create(user)
    return new_user