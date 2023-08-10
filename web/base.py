from fastapi import APIRouter, HTTPException, Request, responses
from fastapi.templating import Jinja2Templates
from apis.route_login import get_current_user_from_token
from db.models.users import User
from web.books import route_books
from web.users import route_users
from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import status

from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


api_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@api_router.get("/")
async def home(
    request: Request, db: Session = Depends(get_db), msg: str = None
):
    """
    Load user home page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    home.html: template
        Load home page
    """
    try:
        token = request.cookies.get("access_token")
        if not token:
            logger.error("Token could not be found")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        scheme, param = get_authorization_scheme_param(token)
        logger.info("Get current user from token")
        current_user: User = get_current_user_from_token(token=param, db=db)
        if current_user:
            logger.info("Redirecting to dashboard")
            return responses.RedirectResponse(
                "/dashboard", status_code=status.HTTP_302_FOUND
            )
    except Exception as e:
        logger.error(f"Exception {e}")
        return templates.TemplateResponse(
            "general_pages/homepage.html", {"request": request}
        )


api_router.include_router(route_books.router, prefix="", tags=["book-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
