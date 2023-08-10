import databases
from db.session import SQLALCHEMY_DATABASE_URL
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


async def check_db_connected():
    """
    Check weather db connected or not

    Parameter
    ---------
    None

    Returns
    -------
    None
    """

    try:
        logger.info("Connecting to DB")
        if not str(SQLALCHEMY_DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(SQLALCHEMY_DATABASE_URL)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
        logger.info("Database is connected")
    except Exception as e:
        logger.error(
            "Looks like db is missing or is there is some problem in connection,see below traceback"
        )
        raise e


async def check_db_disconnected():
    """
    Check weather db disconnected or not

     Parameter
     ---------
     None

     Returns
     -------
     None
    """
    try:
        logger.info("Check DB connection")
        if not str(SQLALCHEMY_DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(SQLALCHEMY_DATABASE_URL)
            if database.is_connected:
                await database.disconnect()
        logger.info("Database is Disconnected")
    except Exception as e:
        logger.error(f"Excetion {e}")
        raise e
