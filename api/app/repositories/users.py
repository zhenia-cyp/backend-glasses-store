from typing import Optional

from app.repositories.base import BaseRepository
from app.models.users import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.database import get_async_session



class UserRepository(BaseRepository):
    """A class for performing asynchronous CRUD operations"""

    async def create(self, data: dict) -> User | None:
        """
        Creates a new user in the database.
        Returns User instance or None if integrity error.
        """
        try:
            new_user = User(**data)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.session.rollback()
            return None


    async def get_by_email(self, email: str) -> User | None:
        """
        Returns user by email or None.
        """
        stmt = select(User).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_phone(self, phone: str) -> Optional[User]:
        stmt = select(User).filter_by(phone=phone)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)