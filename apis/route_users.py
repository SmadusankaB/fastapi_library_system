from util.config import settings
from apis.route_login import get_current_user_from_token
from db.repository.users import (
    get_user_by_user_name,
    update_user_by_username,
)
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.users import ShowUser
from sqlalchemy.orm import Session
from db.models.users import User
from fastapi import HTTPException
from fastapi import status
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

router = APIRouter()


@router.get("/", response_model=ShowUser)
async def get_user(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    """
    REST support for user details

    Parameter
    ---------
    None

    Returns
    -------
    response: ShowUser
        User object
    """

    logger.debug(f"Current user {current_user}")
    logger.info("Get current user by username")
    user = get_user_by_user_name(current_user.username, db=db)
    if not user:
        logger.error("User could not be found")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="User could not be found"
        )
    logger.debug(f"User by username {user}")
    logger.info("User found")
    return user


@router.put("/", response_model=ShowUser)
async def update_user(user: ShowUser, db: Session = Depends(get_db)):
    """
    Update user by username

    Parameter
    ---------
    user: ShowUser
        User details to be updated

    Returns
    -------
    response: ShowUser
        User object
    """

    logger.info("Updating user by user id")
    user = update_user_by_username(user=user, db=db)
    if not user:
        logger.error("User could not be found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User could not be found",
        )
    logger.info("Update has been updated successfully")
    return user


# @router.post("/")
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     user = create_new_user(user=user, db=db)
#     return user
