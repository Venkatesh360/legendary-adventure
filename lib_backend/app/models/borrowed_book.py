from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from ..database.config import Base
from utils.utils import fifteen_days_from_now

class BorrowedBook(Base):
    
    __tablename__ = 'borrowed_books'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    borrower_id = Column(Integer, ForeignKey("users.id"))
    lender_id = Column(Integer, ForeignKey("users.id"))
    lending_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    return_date = Column(DateTime(timezone=True), default=fifteen_days_from_now, nullable=False)
    returned = Column(Boolean, default=False)
    
    book = relationship("Book", back_populates="borrowed_books")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="books_borrowed")
    lender = relationship("User", foreign_keys=[lender_id], back_populates="books_lent")
