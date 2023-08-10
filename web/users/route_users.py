from pydantic import ValidationError
from apis.route_login import (
    get_current_user_from_token,
    login_for_access_token,
)
from db.models.users import User
from db.repository.users import (
    create_new_user,
)
from db.session import get_db
from fastapi import APIRouter, HTTPException, Response
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from web.users.form_user_register import UserCreateForm
from web.users.form_user_login import LoginForm
from fastapi.security.utils import get_authorization_scheme_param

from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    """
    Load user signup page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    register.html: template
        Load sign up page
    """
    logger.info("Request sign up page")
    return templates.TemplateResponse(
        "users/register.html", {"request": request}
    )


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    """
    Submit user signup form

    Parameter
    ---------
    request: Request
       Request object is having user signup data

    Returns
    -------
    homepage.html: template
        on valid signup user will be redirected to home page with succes message
        on invalid signup user will be redirected tp home page with error message
    """
    form = UserCreateForm(request)
    await form.load_data()
    logger.info("Validate user inputs")
    if await form.is_valid():
        logger.info("User registration validated")
        try:
            user = UserCreate(
                username=form.username,
                email=form.email,
                password=form.password,
            )
            logger.info("Create user")
            user = create_new_user(user=user, db=db)
            logger.info("User has been successfully  created")
            return templates.TemplateResponse(
                "general_pages/homepage.html",
                {
                    "request": request,
                    "msg": "Successfully-Registered. Please Login",
                },
            )
        except IntegrityError as e:
            logger.error(f"IntegrityError {e}")
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse(
                "users/register.html", form.__dict__
            )
        except ValidationError as e:
            logger.error(f"ValidationError {e}")
            form.__dict__.get("errors").append(
                "Invalid Input. Password must container atleast 5 charactors and one Uppercase"
            )
            return templates.TemplateResponse(
                "users/register.html", form.__dict__
            )
        except Exception as e:
            logger.error(f"Exception {e}")
            form.__dict__.get("errors").append(f"{e}")
            return templates.TemplateResponse(
                "users/register.html", form.__dict__
            )
    logger.error("Invalid user inputs")
    logger.info("Redirected to sign up page")
    return templates.TemplateResponse("users/register.html", form.__dict__)


@router.get("/login/")
def login(request: Request):
    """
    Load user signin page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    login.html: template
        Load sign in page
    """
    logger.info("Request sign in page")
    return templates.TemplateResponse("users/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    """
    Submit user sign in form

    Parameter
    ---------
    request: Request
       Request object is having user signin data

    Returns
    -------
    homepage.html: template
        on valid signup user will be redirected to dashboard page with succes message
        on invalid signup user will be redirected tp login page with error message
    """
    form = LoginForm(request)
    await form.load_data()
    logger.info("Validate user inputs")
    if await form.is_valid():
        logger.info("User login validated")
        try:
            logger.info("Login successfull!")
            form.__dict__.update(msg="Login Successful :)")
            response = responses.RedirectResponse(
                "/dashboard", status_code=status.HTTP_302_FOUND
            )
            logger.info("Get access token")
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException as e:
            logger.error(f"HTTPException {e}")
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append(
                "Incorrect Username or Password"
            )
            return templates.TemplateResponse(
                "users/login.html", form.__dict__
            )
    logger.error("Invalid user inputs")
    logger.info("Redirected to sign in page")
    return templates.TemplateResponse("users/login.html", form.__dict__)


@router.get("/user/")
async def user(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    """
    Load user account page on the browser

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    account.html: template
        Load user account page
    """
    try:
        logger.debug("Get token from cookies")
        token = request.cookies.get("access_token")
        if not token:
            logger.error("Token could not be found")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        scheme, param = get_authorization_scheme_param(token)
        logger.info("Get current user from token")
        current_user: User = get_current_user_from_token(token=param, db=db)
        if current_user:
            logger.info("Redirected to account page")
            return templates.TemplateResponse(
                "users/account.html", {"request": request}
            )
    except Exception as e:
        logger.error(f"Exception {e}")
        return responses.RedirectResponse(
            "/", status_code=status.HTTP_302_FOUND
        )


@router.get("/logout/")
async def login(
    request: Request, response: Response, db: Session = Depends(get_db)
):
    """
    Load home page on the browser on user logout

    Parameter
    ---------
    request: Request
       Request object

    Returns
    -------
    homepage.html: template
        Load home page
    """
    try:
        logger.info("Redirected to home page on user logout")
        response = responses.RedirectResponse(
            "/", status_code=status.HTTP_302_FOUND
        )
        logger.debug("Delete access token from cookies")
        response.delete_cookie("access_token")
        return response
    except HTTPException as e:
        logger.error(f"HTTPException {e}")
        return templates.TemplateResponse(
            "general_pages/homepage.html",
            {"request": request, "error": f"{str(e.detail)}. Login again! "},
        )
