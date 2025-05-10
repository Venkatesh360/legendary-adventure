from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.utils import get_db, get_token_data, get_user_by_id
from ..models.user import User
from ..models.book import Book
from ..models.borrowed_book import BorrowedBook
from ..schemas import book_schema
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserOutResponse, UserData
import os
import dotenv

dotenv.load_dotenv()

router = APIRouter()

@router.get("/get_all_user", response_model=UserOutResponse)
def get_all_users(user: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    """
    Retrieve a list of all users in the system. Only accessible by admin users.
    
    Args:
        user: The current user making the request.
        db: The database session dependency.
        
    Raises:
        HTTPException: If the user does not have admin privileges.
    
    Returns:
        A list of all users in the database.
    """
    db_user = get_user_by_id(user.get("user_id"), db)  # type: ignore
    
    if not db_user.is_admin:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't have admin level access"
        )
        
    all_users = db.query(User).all()
    return {"users": all_users}


@router.post("/create_admin/{access_key}")
def create_admin(access_key: str, user_data: UserData, db: Session = Depends(get_db)):
    """
    Grant admin access to a user, using an access key to verify request authorization.

    Args:
        access_key: The key to verify the request.
        user_data: The data of the user to grant admin privileges.
        db: The database session dependency.
        
    Raises:
        HTTPException: If the access key is invalid or the user does not exist.
    
    Returns:
        A confirmation message of admin privileges being granted.
    """
    ACCESS_KEY = os.getenv("KEY")
    
    if access_key != ACCESS_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access key"
        )
    
    db_user = get_user_by_id(user_data.user_id, db)
    
    db_user.is_admin = True  # type: ignore
    db.commit()
    db.refresh(db_user)
    
    return {"message": f"user {db_user.username} is granted admin access"}


@router.post("/request_book")
def request_book(req: book_schema.BookRequest, token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    """
    Handle a book borrowing request. The request can only be made by admin users.

    Args:
        req: The book request data (includes book title, author, and user ID).
        token_data: The current user’s authentication data.
        db: The database session dependency.

    Raises:
        HTTPException: If the book is not found, or if no copies are available, or if the user lacks admin access.

    Returns:
        Details about the borrowed book, including expected return date.
    """
    db_user = get_user_by_id(token_data.get("user_id"), db)  # type: ignore
    
    if not db_user.is_admin:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Lending books requires admin level access"
        )
        
    author = req.author.strip().lower()
    title = req.title.strip().lower()
        
    req_book = db.query(Book).filter(Book.title == title, Book.author == author).first()
    
    if not req_book:
        raise HTTPException(status_code=404, detail="Book not found, recheck title and author")
    
    available_copies: int = req_book.available_copies  # type: ignore
        
    if available_copies <= 1: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No copies available"
        )
        
    available_copies -= 1  
    
    req_book.available_copies = available_copies  # type: ignore
    
    db.refresh(req_book)
    
    borrowed = BorrowedBook(
        book_id=req_book.id,
        borrower_id=req.user_id,
        lender_id=token_data.get("user_id")  # type: ignore   
    )
    
    db.commit()
    db.refresh(borrowed)
    
    return {
        "record_id": borrowed.id,
        "title": req_book.title,
        "author": req_book.author,
        "return_by": borrowed.return_date
    }


@router.put("/add_book")
def add_books(new_books: book_schema.AddBook, token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    """
    Add new books to the inventory. Only accessible by admin users.

    Args:
        new_books: The book details (title, author, count).
        token_data: The current user's authentication data.
        db: The database session dependency.

    Raises:
        HTTPException: If the user lacks admin access or the book already exists.
    
    Returns:
        A confirmation message about the new books added to the inventory.
    """
    db_user = get_user_by_id(token_data.get("user_id"), db)  # type: ignore
    
    if not db_user.is_admin:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't have admin level access"
        )
    
    author = new_books.author.strip().lower()
    title = new_books.title.strip().lower()
        
    db_book = db.query(Book).filter(Book.author == author, Book.title == title).first()
    
    if db_book is None:
        db_book = Book(
            title=title,
            author=author
        )
        db.add(db_book)  # Added to the session for persistence
        
    db_book.available_copies += new_books.count  # type: ignore
    
    db.commit()
    
    return {"message": f"{new_books.count} of {new_books.title} by {new_books.author} added to inventory"}
