from sqlalchemy import Column, String, Integer
from ..database.config import Base
from sqlalchemy.orm import relationship



class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    book_name = Column(String, unique=True, nullable=False, index=True)
    author_name = Column(String, index=True, nullable=False)
    cluster_key = Column(String, nullable=False, index=True, unique=True)
    copy_count = Column(Integer, nullable=False)
    
    borrowed_books = relationship("BorrowedBook", back_populates="book")
    
    available_copies = relationship("Inventory", back_populates="book")