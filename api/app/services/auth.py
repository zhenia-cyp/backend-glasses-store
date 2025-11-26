from app.repositories.users import UserRepository
from fastapi import Depends

from app.repositories.users import get_user_repository
from app.models import User
from app.auth.tokens import (
    generate_jwt_token,
    verify_token,
    extract_email_by_token,
    TokenType
)
from app.utils.exceptions import CredentialsException
from app.utils.utils import verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository = Depends(get_user_repository)):
        self.user_repo = user_repo


    async def authenticate(self, password, current_user: User) -> tuple[str, str]:
        if not verify_password(password, current_user.hashed_password):
            raise CredentialsException("Invalid email or password")
        access_token = generate_jwt_token({"sub": current_user.email}, TokenType.ACCESS)
        refresh_token = generate_jwt_token({"sub": current_user.email}, TokenType.REFRESH)
        return access_token, refresh_token


    async def get_user_by_token(self, token: str, token_type: TokenType) -> User:
        payload = verify_token(token, token_type)
        email = extract_email_by_token(payload)
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise CredentialsException("User not found")
        return user


    async def create_email_verify_token(self, email: str) -> str:
        return generate_jwt_token({"sub": email}, TokenType.VERIFY_EMAIL)


    async def verify_email_token(self, token: str) -> str:
        payload = verify_token(token, TokenType.VERIFY_EMAIL)
        return extract_email_by_token(payload)


async def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)



