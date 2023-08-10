from typing import Generator

from util.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Create DB session

    Parameter
    ---------
    None

    Returns
    -------
    db: Session
       yield db session or close
    """
    try:
        logger.info("DB session has been created")
        db = SessionLocal()
        yield db
    finally:
        logger.info("DB session closed")
        db.close()
