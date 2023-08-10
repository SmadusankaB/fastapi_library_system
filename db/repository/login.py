from db.models.users import User
from sqlalchemy.orm import Session


def get_user(username: str, db: Session):
    """
    Get user from db by username

    Parameter
    ---------
    username: str
       Username

    Returns
    -------
    user: User
       User object from db
    """
    user = db.query(User).filter(User.username == username).first()
    return user
