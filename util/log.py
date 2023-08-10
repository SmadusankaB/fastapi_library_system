from pydantic import BaseModel
from util.config import settings


# pydanthic does cls to dict casting
class LogConfig(BaseModel):
    """Logging configuration to be set"""

    LOGGER_NAME: str = settings.LOGGER_NAME
    LOG_FORMAT: str = (
        "%(levelprefix)s %(asctime)s [%(filename)s %(lineno)d] %(message)s"
    )
    LOG_LEVEL: str = settings.LOG_LEVEL
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
