from fastapi import APIRouter, Depends, HTTPException, status
from ..utils.utils import  get_db, get_token_data, get_user_by_id
from ..models.user import User
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserOutResponse,UserData
from typing import List
router = APIRouter()
import os
import dotenv
dotenv.load_dotenv()


@router.get("/get_all_user", response_model=UserOutResponse)
def get_all_users(user: dict = Depends(get_token_data), db: Session = Depends(get_db)):
    
    db_user = get_user_by_id(user.get("user_id"))  #type: ignore
    
    if not db_user.is_admin: #type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't have admin level access"
        )
        
    all_users = db.query(User).all()
    return {"users": all_users}


@router.post("/create_admin/{access_key}")
def create_admin(access_key: str, user_data: UserData, db: Session= Depends(get_db)):
    ACCESS_KEY = os.getenv("KEY")
    print(user_data)
    if access_key != ACCESS_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access key"
            )
    
    db_user = get_user_by_id(user_id=user_data.user_id)
    
    db_user.is_admin = True #type: ignore
    db.commit()
    db.refresh(db_user)
    
    return {"message": f"user {db_user.username} is granted admin access"}
    
   
@router.post("/lend_book")
def lend_book(user :dict = Depends(get_token_data), db: Session = Depends(get_db)):
    
    db_user = get_user_by_id(user.get("user_id")) #type: ignore
    
    if not db_user.is_admin: #type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't have admin level access"
        )