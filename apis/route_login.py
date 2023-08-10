from datetime import timedelta

from apis.utils import OAuth2PasswordBearerWithCookie
from util.config import settings
from util.hashing import Hasher
from util.security import create_access_token
from db.repository.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.tokens import Token
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

router = APIRouter()


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    """
    Authenticate user by username and pssword

    Parameter
    ---------
    username: str
        user username
    password: str
        user password

    Returns
    -------
    response: User
        User object
    """

    logger.info("Autheticating user")
    logger.debug(f"Current user {username}")
    user = get_user(username=username, db=db)
    logger.debug(f"User {user}")
    if not user:
        logger.error("User doesn't exist")
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        logger.error("Password could not be verified")
        return False
    logger.info("User has been successfully authenticated")
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    User login

    Parameter
    ---------
    username: str
        user username
    password: str
        user password

    Returns
    -------
    response: Token
        JWT token
    """

    logger.info("User login")
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.error("User does not exist")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    logger.info("Set token expiration")
    access_token_expires = timedelta(
        minutes=settings.APP_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    logger.debug(f"Token expiration {access_token_expires}")
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info("Access toke has been created successfully")
    logger.info("Sett cookie")
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    logger.info("User login success")
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Get current user information from the token

    Parameter
    ---------
    token: str
        JWT token

    Returns
    -------
    response: Token
        JWT token
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        logger.info("Decoding jwt token")
        payload = jwt.decode(
            token, settings.APP_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        logger.debug(f"username extracted is {username}")
        if username is None:
            logger.error("Username could not be found in token")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Error occured {e}")
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        logger.error("User could not be found")
        raise credentials_exception
    logger.info("User successfuly extracted from token")
    return user
