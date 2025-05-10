from sqlalchemy import Column, String, Integer
from ..database.config import Base
from sqlalchemy.orm import relationship

class Book(Base):
    """
    Represents a book in the library system.

    This class defines the structure of the 'books' table, including fields like:
    - title (unique, non-nullable)
    - author (non-nullable)
    - available_copies (default: 0, non-nullable)
    
    It also establishes a relationship with the 'BorrowedBook' model, linking books to borrow records.
    """
    
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False, index=True)
    author = Column(String, index=True, nullable=False)
    available_copies = Column(Integer, default=0, nullable=False)
    
    # Defining a relationship with the 'BorrowedBook' model
    borrowed_books = relationship("BorrowedBook", back_populates="book")
