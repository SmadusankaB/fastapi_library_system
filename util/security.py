from datetime import datetime
from datetime import timedelta
from typing import Optional
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

from jose import jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token

    Parameter
    ---------
    date : dict
        Data to be embed in token

    expires_delta: timedelta
        Expiration factor

    Returns
    -------
    status: bool
        Return hashed value of password

    """
    logger.info("Set expiration")
    to_encode = data.copy()
    if expires_delta:
        logger.info("Use expires delta")
        expire = datetime.utcnow() + expires_delta
    else:
        logger.info("Use given expires delta")
        expire = datetime.utcnow() + timedelta(
            minutes=settings.APP_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    logger.info("Expiration updated")
    encoded_jwt = jwt.encode(
        to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    logger.info("JWT encoded")
    return encoded_jwt
