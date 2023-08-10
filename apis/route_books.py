import pathlib
from typing import List

from apis.route_login import get_current_user_from_token
from db.models.users import User
from db.repository.books import create_new_book, get_summar
from db.repository.books import delete_book_by_id
from db.repository.books import list_books
from db.repository.books import retreive_book
from db.repository.books import update_book_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.books import BookCreate, Summary
from schemas.books import ShowBook
from sqlalchemy.orm import Session
from util.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


router = APIRouter()

BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
UPLOADS_DEST: str = str(BASE_DIR / "uploads")


@router.post("/create-book/", response_model=ShowBook)
def create_book(
    book: BookCreate,
    # book: BookCreate = Depends(),
    # file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Create/Add book in system.

    Parameter
    ---------
    book: BookCreate
        book object with required parameters

    Returns
    -------
    book: ShowBook
        book cretaed
    """

    # TODO: Complete cover photo upload
    # img_file = file.file
    # img_name = file.filename.replace(" ", "")

    # print(book)
    # is_exist = os.path.exists(UPLOADS_DEST)
    # if not is_exist:
    #     os.makedirs(UPLOADS_DEST)

    # timestr = time.strftime("%Y%m%d_%H%M%S")
    # path = f"{UPLOADS_DEST}/{timestr}_{img_name}"
    # img_PIL = Image.open(img_file)
    # img_PIL.save(path)

    # is_file_exist = os.path.exists(path)

    # if not is_file_exist:
    #     raise Exception("Image upload failed")

    try:
        logger.info("Creating  book")
        book = create_new_book(book=book, db=db, owner_id=current_user.id)
        logger.info("Book has been created")
        logger.debug(f"Created book: {book}")
        return book
    except Exception as e:
        logger.error(f"Exception {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data Integrity error. Check data you have entered and try again.",
        )


@router.get("/get/{id}", response_model=ShowBook)
def read_book(id: int, db: Session = Depends(get_db)):
    """
    Get book by book id

    Parameter
    ---------
    id: int
        book id

    Returns
    -------
    book: ShowBook
        book match with id
    """
    try:
        logger.info("Getting  book")
        logger.debug(f"Book ID {id}")
        book = retreive_book(id=id, db=db)
        if not book:
            logger.error("Book could not be found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with this id {id} does not exist",
            )
        logger.debug(f"Book: {book}")
        return book
    except Exception as e:
        logger.error(f"Exception {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occured {e}",
        )


@router.get("/all", response_model=List[ShowBook])
def read_books(db: Session = Depends(get_db)):
    """
    Get all book in the system

    Parameter
    ---------
    None

    Returns
    -------
    books: List[ShowBook]
        List of books avaialable in the system
    """

    logger.info("Getting all books")
    books = list_books(db=db)
    logger.debug(f"Books to be returned {books}")
    return books


@router.put("/update/{id}")
def update_books(id: int, book: BookCreate, db: Session = Depends(get_db)):
    """
    Update book by id

    Parameter
    ---------
    id: int
        book id

    Returns
    -------
    response: dict
        Just notify user about updation satus
    """
    current_user = 1
    try:
        logger.info("Updating book")
        logger.debug(f"Book id {id}")
        message = update_book_by_id(
            id=id, book=book, db=db, owner_id=current_user
        )
        logger.debug(f"Book update status {message}")
        if not message:
            logger.error("Updatetion failed or book could not be found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {id} not found",
            )
        return {"msg": "Successfully updated data."}
    except Exception as e:
        logger.error(f"Exception occured {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data Integrity error",
        )


@router.delete("/delete/{id}")
def delete_book(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Delete book by id

    Parameter
    ---------
    id: int
        book id

    Returns
    -------
    response: dict
        Just notify user about updation satus
    """

    book = retreive_book(id=id, db=db)
    if not book:
        logger.error("Book could not be found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} does not exist",
        )
    logger.debug(
        f"{book.owner_id}, {current_user.id}, {current_user.is_superuser}"
    )
    if book.owner_id == current_user.id or current_user.is_superuser:
        res = delete_book_by_id(id=id, db=db, owner_id=current_user.id)
        if not res:
            logger.error("Book could not be found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item could not be found",
            )
        logger.info("Book has been successfully deleted")
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not permitted!!!!",
    )


@router.get("/summary", response_model=Summary)
def get_summary(db: Session = Depends(get_db)):
    """
    Update book by id

    Parameter
    ---------
    id: int
        book id

    Returns
    -------
    response: dict
        Just notify user about updation satus
    """

    try:
        sum = get_summar(db=db)
        return sum
    except Exception as e:
        logger.error(f"Exception occured {e}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occured",
        )
