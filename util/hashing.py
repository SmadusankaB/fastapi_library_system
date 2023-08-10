from passlib.context import CryptContext
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    This class manage password hasing
    """

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify hashed password

        Parameter
        ---------
        plain_password : str
            Plain text password

        hashed_password : str
            Hahed password

        Returns
        -------
        status: bool
            Return verification status

        """
        logger.info("Verify password")
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        Get password hash value

        Parameter
        ---------
        password : str
            Plain text password

        Returns
        -------
        status: bool
            Return hashed value of password

        """
        logger.info("Get hashed password")
        return pwd_context.hash(password)
