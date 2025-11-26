from datetime import datetime, timedelta
from app.core.config import settings
from app.schemas.users import TokenPayload
import jwt
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from app.utils.exceptions import CredentialsException, TokenExpiredException
from app.schemas.enum import TokenType


# def generate_jwt_token(data: dict, token_type: TokenType) -> str:
#     payload = data.copy()
#     if token_type == TokenType.ACCESS:
#         expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     else:
#         expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES
#     issued_at = datetime.utcnow()
#     payload["iat"] = issued_at
#     payload["exp"] = issued_at + timedelta(minutes=expire_minutes)
#     payload["type"] = token_type.value
#     return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
def generate_jwt_token(data: dict, token_type: TokenType) -> str:
    payload = data.copy()

    if token_type == TokenType.ACCESS:
        expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    elif token_type == TokenType.REFRESH:
        expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    elif token_type == TokenType.VERIFY_EMAIL:
        expire_minutes = settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES
    else:
        raise ValueError(f"Unsupported token type: {token_type}")

    issued_at = datetime.utcnow()
    payload["iat"] = issued_at
    payload["exp"] = issued_at + timedelta(minutes=expire_minutes)
    payload["type"] = token_type.value

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, token_type: TokenType) -> dict:
    try:
        return jwt_decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException(f"{token_type.value} token has expired")
    except InvalidTokenError:
        raise CredentialsException(f"Invalid {token_type.value} token")


def validate_token(payload: TokenPayload, seconds: int = 30) -> TokenPayload:
    now = datetime.utcnow().timestamp()
    if payload.iat > now + seconds:
        raise CredentialsException("Token is invalid: it was issued for a future time")
    if payload.exp <= payload.iat:
        raise CredentialsException("Expiration time must be after issuance time")
    return payload


def verify_token(token: str, token_type: TokenType) -> TokenPayload:
    payload = decode_token(token, token_type)
    validated = validate_token(TokenPayload(**payload))
    if validated.type != token_type.value:
        raise CredentialsException(
            f"Invalid token type: expected '{token_type.value}', got '{validated.type}'"
        )
    return validated


def extract_email_by_token(payload: TokenPayload) -> str:
    if not payload.sub:
        raise CredentialsException("Token has no subject")
    return payload.sub


