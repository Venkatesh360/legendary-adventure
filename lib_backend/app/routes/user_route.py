from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.utils import get_token_data, get_db
from ..models.user import User

router = APIRouter()


@router.get("/get_borrowed_books")
def get_borrowed_books(token_data: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    user_id = token_data.get("user_id")
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    
    return db_user.books_borrowed