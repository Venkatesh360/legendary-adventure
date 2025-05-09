from sqlalchemy import Column, String, Integer
from ..database.config import Base
from sqlalchemy.orm import relationship



class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False, index=True)
    author = Column(String, index=True, nullable=False)
    available_copies = Column(Integer, default=0 ,nullable=False)
    
    borrowed_books = relationship("BorrowedBook", back_populates="book")