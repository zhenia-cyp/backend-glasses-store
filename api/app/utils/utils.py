from passlib.context import CryptContext
from app.core.templates import templates


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_welcome_message(verify_link: str) -> str:
    template = templates.get_template("welcome_email.html")
    return template.render(verify_link=verify_link)







