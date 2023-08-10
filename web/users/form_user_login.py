from typing import List
from typing import Optional

from fastapi import Request
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


class LoginForm:
    """
    LoginForm class represent user login form
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
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
        logger.debug("Create LoginForm object")
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        """
        Validate user inputs

        Parameter
        ---------
        self: LoginForm
            LoginForm is having form data

        Returns
        -------
        bool:
            Return true or false based on user inputs
        """
        if not self.username:
            logger.error("Invalid username")
            self.errors.append("Username is required")
        if not self.password or not len(self.password) >= 4:
            logger.error("Invalid password")
            self.errors.append("A valid password is required")
        if not self.errors:
            logger.error("Invalid login inputs")
            return True
        logger.info("Valid user login inputs")
        return False
