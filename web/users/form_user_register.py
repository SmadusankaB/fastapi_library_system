from typing import List
from typing import Optional
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

from fastapi import Request


class UserCreateForm:
    """
    UserCreateForm class represent user registration form
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        """
        Load form data and create form object

        Parameter
        ---------
        request: Request
        Request object is having form data

        Returns
        -------
        None
        """
        logger.debug("Create UserCreateForm object")
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        """
        Validate user inputs

        Parameter
        ---------
        self: UserCreateForm
            UserCreateForm is having form data

        Returns
        -------
        bool:
            Return true or false based on user inputs
        """
        if not self.username or not len(self.username) > 3:
            logger.error("Invalid username")
            self.errors.append("Username should be > 3 chars")
        if not self.email or not (self.email.__contains__("@")):
            logger.error("Invalid email")
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            logger.error("Invalid password")
            self.errors.append("Password must be > 4 chars")
        if not self.errors:
            return True
        logger.info("Valid user registration inputs")
        return False
