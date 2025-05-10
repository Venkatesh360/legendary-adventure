from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from ..database.config import Base
from ..utils.utils import fifteen_days_from_now

class BorrowedBook(Base):
    """
    Represents the record of a borrowed book.

    This class defines the structure of the 'borrowed_books' table, which keeps track
    of the books borrowed from the library, along with the borrower and lender information, 
    lending date, and return status.
    """
    
    __tablename__ = 'borrowed_books'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to the 'books' table
    book_id = Column(Integer, ForeignKey("books.id"), index=True)
    
    # Foreign keys to the 'users' table (borrower and lender)
    borrower_id = Column(Integer, ForeignKey("users.id"), index=True)
    lender_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Lending and return details
    lending_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    return_date = Column(DateTime(timezone=True), default=fifteen_days_from_now, nullable=False)
    
    # Status to track if the book has been returned
    returned = Column(Boolean, default=False)
    
    # Relationships with other models (Book and User)
    book = relationship("Book", back_populates="borrowed_books")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="books_borrowed")
    lender = relationship("User", foreign_keys=[lender_id], back_populates="books_lent")
