from apis.route_login import get_current_user_from_token
from db.models.users import User
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import HTTPException

from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/dashboard/")
async def dashboard(
    request: Request, db: Session = Depends(get_db), msg: str = None
):
    """
    Load dashboard page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    dashboard.html: template
        Load dashboard page
    """
    try:
        logger.info("Request dashboard page")
        token = request.cookies.get("access_token")
        if not token:
            logger.error("Invalid credentials")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        scheme, param = get_authorization_scheme_param(token)
        logging.info("Get current user from token")
        current_user: User = get_current_user_from_token(token=param, db=db)
        if current_user:
            logger.info("Return dashboard page")
            return templates.TemplateResponse(
                "general_pages/dashboard.html", {"request": request}
            )
    except Exception as e:
        logger.error(f"Exception occured {e}")
        return responses.RedirectResponse(
            "/", status_code=status.HTTP_302_FOUND
        )


@router.get("/books/")
def book_detail(request: Request, db: Session = Depends(get_db)):
    """
    Load my books page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    my_books.html: template
        Load my books page
    """
    try:
        logger.info("Request my_books page")
        token = request.cookies.get("access_token")
        if not token:
            logger.error("Invalid credentials")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        scheme, param = get_authorization_scheme_param(token)
        logging.info("Get current user from token")
        current_user: User = get_current_user_from_token(token=param, db=db)
        if current_user:
            logger.info("Return my_books page")
            return templates.TemplateResponse(
                "books/my_books.html", {"request": request}
            )
    except Exception as e:
        logger.error(f"Exception occured {e}")
        return responses.RedirectResponse(
            "/", status_code=status.HTTP_302_FOUND
        )
