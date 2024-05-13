from fastapi import HTTPException
from sqlmodel import Session, select

from app.api_models import RegisterUserResponse, RegisterUserRequest
from app.core.database import engine
from app.core.security import hash_password
from app.db_models import User


def get_user_by_email(email) -> User:
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        return user


def verify_email_is_unique(email: str):
    user = get_user_by_email(email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=f"User with email: {email} already exists!"
        )


def register_user(user_in: RegisterUserRequest) -> User:
    verify_email_is_unique(user_in.email)
    user_obj = User.model_validate(user_in, update={"password": hash_password(user_in.password)})
    with Session(engine) as session:
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)
    return user_obj
