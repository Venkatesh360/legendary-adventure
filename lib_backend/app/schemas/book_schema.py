from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BookRequest(BaseModel):
    """
    Schema for requesting to borrow a book.

    Attributes:
        user_id (int): ID of the user making the request.
        title (str): Title of the book.
        author (str): Author of the book.
    """
    user_id: int
    title: str
    author: str


class AddBook(BaseModel):
    """
    Schema for adding books to the inventory.

    Attributes:
        title (str): Title of the book.
        author (str): Author of the book.
        count (int): Number of copies to be added.
    """
    title: str
    author: str
    count: int


class AllBook(BaseModel):
    """
    Schema representing a book in the system.

    Attributes:
        id (int): Book ID.
        title (str): Title of the book.
        author (str): Author of the book.
    """
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True  # Enables support for ORM objects


class BookListRequest(BaseModel):
    """
    Schema representing a list of books.

    Attributes:
        books (List[AllBook]): List of book entries.
    """
    books: List[AllBook]


class BorrowedBookResponse(BaseModel):
    """
    Schema representing a borrowed book record.

    Attributes:
        borrowed_book_id (int): ID of the borrowed book record.
        title (str): Title of the borrowed book.
        author (str): Author of the borrowed book.
        borrowed_date (datetime): Date when the book was borrowed.
        return_date (datetime): Expected return date.
        returned (bool): Indicates whether the book has been returned.
    """
    borrowed_book_id: int
    title: str
    author: str
    borrowed_date: datetime
    return_date: datetime
    returned: bool

    class Config:
        orm_mode = True  # Enables support for ORM objects
