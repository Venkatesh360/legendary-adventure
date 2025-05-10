from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.utils import get_token_data, get_db, get_user_by_id
from ..models.book import Book
from ..schemas.book_schema import BookListRequest
from typing import List

router = APIRouter()

@router.get("/get_all", response_model=List[BookListRequest])
def get_all_books(token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    """
    Endpoint to fetch all books with more than one available copy.

    Args:
        token_data: The decoded JWT token data, including the user_id.
        db: The database session dependency.

    Raises:
        HTTPException: If the user is not found in the database.

    Returns:
        A list of books with more than one available copy.
    """
    # Retrieve the user from the database using the user_id from the token
    db_user = get_user_by_id(token_data.get("user_id"), db)  # type: ignore
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # Changed to 404 for user not found
            detail="User not a registered user"
        )
        
    # Fetch all books with more than one available copy
    books = db.query(Book).filter(Book.available_copies > 1).all()
    
    # Return the list of books 
    return {"books": books}
