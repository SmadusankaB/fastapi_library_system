from util.hashing import Hasher
from db.models.users import User
from schemas.users import ShowUser, UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    """
    Create  a new user in db

    Parameter
    ---------
    user : UserCreate
       New user details

    Returns
    -------
    user: User
       Newly created user
    """
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    user_exist = db.query(User).filter(User.username == user.username).first()
    if user_exist:
        raise Exception("User already exists")

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    """
    Get user from db by email

    Parameter
    ---------
    email : str
       User email address

    Returns
    -------
    user: User
       User object
    """
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_by_user_name(username: str, db: Session):
    """
    Get user from db by username

    Parameter
    ---------
    username : str
       User username

    Returns
    -------
    user: User
       User object
    """
    user = db.query(User).filter(User.username == username).first()
    return user


def update_user_by_username(user: ShowUser, db: Session):
    """
    Update user in db by username

    Parameter
    ---------
    user : ShowUser
      New user details

    Returns
    -------
    user: User
       User object
    """
    existing_user = db.query(User).filter(User.username == user.username)
    if not existing_user:
        return 0
    existing_user.update(user.__dict__)
    db.commit()
    return user
