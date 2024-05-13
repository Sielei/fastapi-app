from sqlmodel import create_engine, Session, SQLModel
from app.core.config import Settings
from app.db_models import User
from app.api_models import RegisterUserRequest


settings = Settings()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
