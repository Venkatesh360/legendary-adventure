from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.utils import get_token_data, get_db
from ..models.borrowed_book import BorrowedBook
from ..models.book import Book 
from ..schemas.book_schema import BorrowedBookResponse
from typing import List

router = APIRouter()

@router.get("/get_borrowed_books", response_model=List[BorrowedBookResponse])
def get_borrowed_books(token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    """
    Retrieve the list of books currently borrowed by the authenticated user.
    """
    user_id = token_data.get("user_id")

    # Query the borrowed books and join with book details based on book_id.
    borrowed_books = (
        db.query(BorrowedBook, Book)
        .join(Book, Book.id == BorrowedBook.book_id)
        .filter(BorrowedBook.borrower_id == user_id)
        .all()
    )

    # Construct the response using the BorrowedBookResponse schema.
    result = [
        BorrowedBookResponse(
            borrowed_book_id=borrowed.id,
            title=book.title,
            author=book.author,
            borrowed_date=borrowed.lending_date,
            returned=borrowed.returned,
            return_date=borrowed.return_date
        )
        for borrowed, book in borrowed_books
    ]

    return result
