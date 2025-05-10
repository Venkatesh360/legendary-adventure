from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from ..database.config import Base
from sqlalchemy.orm import relationship
from .borrowed_book import BorrowedBook


class TimestampMixin:
    """
    Mixin that automatically adds timestamp fields for creation and last update.

    This mixin can be inherited by models to automatically manage:
    - `created_at`: The timestamp when the record is first created (set automatically).
    - `updated_at`: The timestamp when the record was last updated (set automatically).
    
    Both fields use SQLAlchemy's `func.now()` to set their values. The `updated_at`
    field is updated on every modification to the record.
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    """
    Represents a user in the system.

    This class defines the structure of the 'users' table, which stores user-related information:
    - `username`: Unique identifier for the user.
    - `email`: User's email address (unique and indexed).
    - `hashed_password`: The user's password (hashed for security).
    - `is_admin`: A boolean indicating if the user has administrative privileges.
    - `created_at` and `updated_at`: Automatic timestamps for creation and last update.

    Relationships:
    - Each user can borrow and lend books (via the `BorrowedBook` model).
    """
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    # Relationship with BorrowedBook: Books borrowed by and lent by the user
    books_borrowed = relationship("BorrowedBook", foreign_keys=[BorrowedBook.borrower_id], back_populates="borrower")
    books_lent = relationship("BorrowedBook", foreign_keys=[BorrowedBook.lender_id], back_populates="lender")
