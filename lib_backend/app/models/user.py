from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from ..database.config import Base
from sqlalchemy.orm import relationship
from .borrowed_book import BorrowedBook


class TimestampMixin:
    """
            Mixin that adds automatic timestamp fields for creation and last update.

            Attributes:
                created_at (DateTime): The timestamp when the record was created.
                    - Automatically set to the current time when the row is inserted.
                
                updated_at (DateTime): The timestamp when the record was last updated.
                    - Automatically set to the current time when the row is inserted.
                    - Automatically updated to the current time whenever the row is updated.
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    
    books_borrowed = relationship("BorrowedBook", foreign_keys=[BorrowedBook.borrower_id], back_populates="borrower")
    books_lent = relationship("BorrowedBook", foreign_keys=[BorrowedBook.lender_id], back_populates="lender")
