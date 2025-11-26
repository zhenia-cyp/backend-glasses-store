from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import User
from app.repositories.users import UserRepository, get_user_repository
from fastapi import Depends
from app.schemas.users import UserCreate, UserRead
from app.utils.utils import get_hash_password
from app.services.auth import get_auth_service
from app.services.auth import AuthService
from app.core.config import settings
from app.celery_tasks.tasks import email_send
from app.utils.utils import create_welcome_message


class UserService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository),
                 auth_service: AuthService = Depends(get_auth_service)):
        self.user_repo = user_repo
        self.auth_service = auth_service


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
        token = await self.auth_service.create_email_verify_token(new_user.email)
        verify_link = f"{settings.EMAIL_VERIFICATION_URL}/?token={token}"
        text = create_welcome_message(verify_link)
        email_send.delay(new_user.email, "Вітаємо в оптиці", text)
        return UserRead.model_validate(new_user)


    async def update(self, user_id: int, data: dict) -> Optional[UserRead]:
        """this method updates an existing user in the database."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
        return await self.user_repo.update(user_id, data)


    async def get_by_email(self, email: str) -> Optional[UserRead]:
        return await self.user_repo.get_by_email(email)


async def get_user_service(repo: UserRepository = Depends(get_user_repository),
                           auth: AuthService = Depends(get_auth_service)) -> UserService:
    return UserService(repo, auth)