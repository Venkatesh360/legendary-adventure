from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Boolean
from ..database.config import Base
from sqlalchemy.orm import relationship

class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True)
    cluster_key = Column(String, ForeignKey("books.cluster_key"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_present = Column(Boolean, default=True)
    
    book = relationship("Book", back_populates="available_copies")
