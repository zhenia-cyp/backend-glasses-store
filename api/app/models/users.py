from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    role: Mapped[str] = mapped_column(nullable=True)


    def __str__(self) -> str:
        return f"User(id={self.id}, firstname='{self.firstname}', lastname='{self.lastname}', " \
               f"email='{self.email}', phone='{self.phone}', role='{self.role}'"


    def __repr__(self) -> str:
        return f"User(id={self.id}, firstname='{self.firstname}', lastname='{self.lastname}', " \
               f"email='{self.email}', phone='{self.phone}', role='{self.role}'"












