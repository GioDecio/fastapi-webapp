from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  # .db file is created automatically

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Factory that creates a db sesssion.
# autocommit=False, autoflush=False: controls when changes are commited


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


# Session is not created in each route, it is injected
def get_db() -> Session:
    with SessionLocal() as db:
        yield db  # This makes the session work as a context manager
