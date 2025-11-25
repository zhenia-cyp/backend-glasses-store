from fastapi import APIRouter, Depends, HTTPException, status

from app.models import User
from app.repositories.users import UserRepository, get_user_repository
from fastapi import Depends
from app.schemas.users import UserCreate, UserRead
from app.utils.utils import get_hash_password


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self.user_repo = user_repo

    async def create(self, user: UserCreate) -> UserRead:
        existing_user = await self.get_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        existing_phone_user = await self.user_repo.get_by_phone(user.phone)
        if existing_phone_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone already exists"
            )
        hashed_password = get_hash_password(user.password)
        user_dict = user.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        new_user = await self.user_repo.create(user_dict)
        return UserRead.model_validate(new_user)


    async def get_by_email(self, email: str) -> User:
        return await self.user_repo.get_by_email(email)


async def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)