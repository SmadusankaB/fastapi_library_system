import datetime
from db.models.books import Book
from schemas.books import BookCreate
from sqlalchemy.orm import Session


def create_new_book(
    book: BookCreate, db: Session, owner_id: int, file_path: str = ""
):
    """
    Create a new book in DB

    Parameter
    ---------
    book: BookCreate
       Book information

    Returns
    -------
    book_object: Book
        Book object to be returned
    """

    book_object = Book(**book.dict(), owner_id=owner_id)
    book_object.cover_path = file_path
    db.add(book_object)
    db.commit()
    db.refresh(book_object)
    return book_object


def retreive_book(id: int, db: Session):
    """
    Get book from db by book id

    Parameter
    ---------
    id: str
       Book id

    Returns
    -------
    book: Book
        Book object to be returned
    """

    book = db.query(Book).filter(Book.id == id).first()
    return book


def list_books(db: Session):
    """
    Get book list of book

    Parameter
    ---------
    None

    Returns
    -------
    books: list[Book]
        List of books to be returned
    """
    books = db.query(Book).all()
    b = []
    for book in books:
        b.append(book)
    return books


def update_book_by_id(id: int, book: BookCreate, db: Session, owner_id):
    """
    Update book in db by book id

    Parameter
    ---------
    id: str
       Book id

    book: BookCreate
        Book information

    Returns
    -------
    status: int
        Notify update status
    """

    existing_book = db.query(Book).filter(Book.id == id)
    if not existing_book.first():
        return 0
    book.__dict__.update(owner_id=owner_id)
    existing_book.update(book.__dict__)
    db.commit()
    return 1


def delete_book_by_id(id: int, db: Session, owner_id):
    """
    Delete book from db by book id

    Parameter
    ---------
    id: str
       Book id

    Returns
    -------
    status: int
        Notify delete status
    """

    existing_book = db.query(Book).filter(Book.id == id)
    if not existing_book.first():
        return 0
    existing_book.delete(synchronize_session=False)
    db.commit()
    return 1


def search_book(query: str, db: Session):
    books = db.query(Book).filter(Book.title.contains(query))
    return books


def get_summar(db: Session):
    """
    Get summary about book

    Parameter
    ---------
    None

    Returns
    -------
    sum: count + list[Book]
       Book cound and list of books
    """

    sum = {}
    count = db.query(Book).count()
    sum["count"] = count
    previous_date = datetime.datetime.today() - datetime.timedelta(days=10)
    items = db.query(Book).filter(
        Book.date_posted >= previous_date.strftime("%Y-%m-%d")
    )
    j = []
    for book in items:
        j.append(book)
    sum["books"] = j
    return sum
